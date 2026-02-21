import argparse
import hashlib
import json
import logging
import os
import random
import re
import threading
import time
from dataclasses import dataclass, asdict
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from urllib.parse import quote_plus

import requests

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
POLLINATIONS_BASE_URL = "https://gen.pollinations.ai/image"
DEFAULT_POSTER_PATH = Path("poster.png")
STATE_FILE = Path("schedule_state.json")
LOG_FILE = Path("autopost.log")

STATE_LOCK = threading.Lock()

TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}


# -----------------------------------------------------------------------------
# Data model
# -----------------------------------------------------------------------------

@dataclass
class MovieData:
    movie_name: str
    hero_name: str
    heroine_name: str
    director_name: str
    genre: str
    release_date: Optional[str] = None
    requirements_poster: Optional[str] = None


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


# -----------------------------------------------------------------------------
# Validation and helpers
# -----------------------------------------------------------------------------

def validate_inputs(data: MovieData) -> None:
    required_fields = {
        "movie_name": data.movie_name,
        "hero_name": data.hero_name,
        "heroine_name": data.heroine_name,
        "director_name": data.director_name,
        "genre": data.genre,
    }

    for key, value in required_fields.items():
        if not value or not value.strip():
            raise ValueError(f"Invalid input: '{key}' is required and cannot be empty.")

    if data.release_date:
        try:
            datetime.strptime(data.release_date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("release_date must be in YYYY-MM-DD format.") from exc


def load_dotenv_file(path: Path = Path(".env")) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_page_credentials() -> Dict[str, str]:
    load_dotenv_file()

    page_id = os.getenv("FB_PAGE_ID", "").strip()
    page_access_token = os.getenv("FB_PAGE_ACCESS_TOKEN", "").strip()

    if page_id and page_access_token:
        return {"page_id": page_id, "page_access_token": page_access_token}

    config_path = Path("config.json")
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        page_id = page_id or str(data.get("page_id", "")).strip()
        page_access_token = page_access_token or str(data.get("page_access_token", "")).strip()

    if not page_id or not page_access_token:
        raise EnvironmentError(
            "Missing credentials. Set FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN in .env, "
            "or provide page_id/page_access_token in config.json."
        )

    return {"page_id": page_id, "page_access_token": page_access_token}


def normalize_movie_key(data: MovieData) -> str:
    base = "|".join(
        [
            data.movie_name.strip().lower(),
            data.hero_name.strip().lower(),
            data.heroine_name.strip().lower(),
            data.director_name.strip().lower(),
            data.genre.strip().lower(),
            (data.release_date or "").strip().lower(),
        ]
    )
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def request_with_retry(
    method: str,
    url: str,
    *,
    max_retries: int = 4,
    timeout: int = 30,
    backoff_base: float = 1.5,
    **kwargs: Any,
) -> requests.Response:
    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.request(method, url, timeout=timeout, **kwargs)
            if response.status_code in TRANSIENT_HTTP_CODES and attempt < max_retries:
                sleep_s = backoff_base ** attempt
                logging.warning(
                    "Transient HTTP %s for %s. Retry %s/%s in %.1fs",
                    response.status_code,
                    url,
                    attempt,
                    max_retries,
                    sleep_s,
                )
                time.sleep(sleep_s)
                continue
            return response
        except requests.RequestException as exc:
            last_error = exc
            if attempt < max_retries:
                sleep_s = backoff_base ** attempt
                logging.warning(
                    "Network error for %s. Retry %s/%s in %.1fs: %s",
                    url,
                    attempt,
                    max_retries,
                    sleep_s,
                    exc,
                )
                time.sleep(sleep_s)
            else:
                break

    raise RuntimeError(f"Request failed after {max_retries} attempts: {last_error}")


# -----------------------------------------------------------------------------
# State management
# -----------------------------------------------------------------------------

def load_state(path: Path = STATE_FILE) -> Dict[str, Any]:
    if not path.exists():
        return {"version": 1, "used_caption_hashes": [], "jobs": []}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: Dict[str, Any], path: Path = STATE_FILE) -> None:
    temp_path = path.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    temp_path.replace(path)


def get_used_caption_hashes(state: Dict[str, Any]) -> Set[str]:
    return set(state.get("used_caption_hashes", []))


def add_used_caption_hash(state: Dict[str, Any], caption_hash: str) -> None:
    used = set(state.get("used_caption_hashes", []))
    used.add(caption_hash)
    state["used_caption_hashes"] = sorted(used)


def upsert_job(state: Dict[str, Any], job: Dict[str, Any]) -> None:
    jobs = state.setdefault("jobs", [])
    for idx, existing in enumerate(jobs):
        if existing.get("job_id") == job.get("job_id"):
            jobs[idx] = job
            return
    jobs.append(job)


def get_job_by_id(state: Dict[str, Any], job_id: str) -> Optional[Dict[str, Any]]:
    for job in state.get("jobs", []):
        if job.get("job_id") == job_id:
            return job
    return None


# -----------------------------------------------------------------------------
# Poster generation
# -----------------------------------------------------------------------------

def build_prompt(data: Dict[str, Any], variation: Optional[str] = None) -> str:
    movie = data["movie_name"]
    hero = data["hero_name"]
    heroine = data["heroine_name"]
    director = data["director_name"]
    genre = data["genre"]
    release_date = data.get("release_date")
    requirements_poster = str(data.get("requirements_poster", "")).strip()

    genre_mood_map = {
        "action": "adrenaline-charged, explosive, gritty",
        "romance": "warm, dreamy, emotional",
        "thriller": "tense, mysterious, high-stakes",
        "horror": "ominous, unsettling, atmospheric",
        "drama": "intense, emotional, character-driven",
        "fantasy": "mythic, magical, breathtaking",
        "sci-fi": "futuristic, sleek, awe-inspiring",
        "comedy": "vibrant, energetic, playful",
    }

    mood = genre_mood_map.get(genre.strip().lower(), "cinematic, dramatic, immersive")
    rd_line = f" Releasing on {release_date}." if release_date else ""
    var_line = f" Visual variant: {variation}." if variation else ""
    req_line = (
        f" Additional poster requirements: {requirements_poster}."
        if requirements_poster
        else ""
    )

    return (
        f"Create a cinematic {genre} movie poster for the film '{movie}' starring "
        f"{hero} and {heroine}, directed by {director}.{rd_line} "
        f"Tone: {mood}. Dramatic lighting, volumetric shadows, ultra-detailed textures, "
        f"high contrast, epic composition, premium typography space, professional film "
        f"marketing poster, award-winning design style, 8k detail, studio-quality finish."
        f"{var_line}{req_line}"
    )


def generate_poster(
    data: Dict[str, Any],
    output_path: str = str(DEFAULT_POSTER_PATH),
    variation: Optional[str] = None,
) -> str:
    prompt = build_prompt(data, variation=variation)
    encoded_prompt = quote_plus(prompt)
    api_key = os.getenv("POLLINATIONS_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError("Missing env var: POLLINATIONS_API_KEY.")

    url = f"{POLLINATIONS_BASE_URL}/{encoded_prompt}?model=flux&key={quote_plus(api_key)}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = request_with_retry("GET", url, headers=headers, max_retries=4, timeout=60)
    if not response.ok:
        raise RuntimeError(f"Poster generation failed: HTTP {response.status_code} | {response.text}")

    path = Path(output_path)
    path.write_bytes(response.content)
    logging.info("Poster saved to %s", path)
    return str(path)


# -----------------------------------------------------------------------------
# Caption generation (LLM-ready interface)
# -----------------------------------------------------------------------------

def _caption_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def generate_caption(data: Dict[str, Any], used_caption_hashes: Optional[Set[str]] = None) -> str:
    used_caption_hashes = used_caption_hashes or set()

    movie = data["movie_name"]
    hero = data["hero_name"]
    heroine = data["heroine_name"]
    director = data["director_name"]
    genre = data["genre"]
    release_date = data.get("release_date")

    release_phrase = f" in theatres on {release_date}" if release_date else " very soon"

    templates = [
        f"Lights, camera, goosebumps! 🎬 {movie} is bringing pure {genre} energy{release_phrase}. "
        f"Starring {hero} and {heroine}, crafted by {director}. Are you ready for the big-screen blast? 🔥 "
        f"Tag your movie squad now! #MovieNight #ComingSoon #CinemaLovers #MustWatch",
        f"The wait ends with {movie}! 🍿 A powerful {genre} spectacle featuring {hero} and {heroine}, "
        f"directed by {director}{release_phrase}. Hit like if this is on your watchlist! 🚀 "
        f"#NewMovie #BigScreenMagic #FilmBuzz #WeekendPlans",
        f"An epic cinematic ride is loading... ⚡ {movie} delivers unforgettable {genre} vibes with "
        f"{hero} and {heroine} under {director}'s vision{release_phrase}. "
        f"Drop a ❤️ if you're excited and share this with friends! #Blockbuster #MoviePromo #ComingSoon #WatchThis",
        f"Posters up, hype on! 🎥 {movie} is set to redefine {genre} entertainment with {hero} + {heroine}, "
        f"directed by {director}{release_phrase}. Book your excitement early and follow for updates! 🙌 "
        f"#CinemaUpdate #FilmFans #UpcomingRelease #MovieAlert",
        f"This is not just a film, it's an event! 🌟 {movie} starring {hero} and {heroine}, directed by {director}, "
        f"brings intense {genre} storytelling{release_phrase}. Comment 'READY' if you're in! 👇 "
        f"#FilmCommunity #TheatreExperience #NewRelease #MustSee",
        f"Get ready for a visual storm! 🎞️ {movie} is arriving with {genre} thrills, featuring {hero} and {heroine}, "
        f"helmed by {director}{release_phrase}. Save this post and share the hype! 🔊 "
        f"#MovieTime #CinematicExperience #ComingSoon #DontMiss",
    ]

    random.shuffle(templates)

    for caption in templates:
        h = _caption_hash(caption)
        if h not in used_caption_hashes:
            return caption

    suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    fallback = (
        f"{movie} is coming{release_phrase}! 🎬 A {genre} cinematic experience starring {hero} and {heroine}, "
        f"directed by {director}. Stay tuned and spread the word! #{suffix} #ComingSoon #MovieBuzz"
    )
    return fallback


# -----------------------------------------------------------------------------
# Facebook posting
# -----------------------------------------------------------------------------

def post_to_facebook(
    page_id: str,
    page_access_token: str,
    image_path: str,
    caption: str,
) -> Dict[str, Any]:
    endpoint = f"{GRAPH_BASE_URL}/{page_id}/photos"

    with open(image_path, "rb") as image_file:
        files = {"source": image_file}
        data = {
            "access_token": page_access_token,
            "caption": caption,
            "published": "true",
        }
        response = request_with_retry("POST", endpoint, files=files, data=data, max_retries=4, timeout=60)

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if not response.ok:
        raise RuntimeError(f"Facebook post failed: HTTP {response.status_code} | {payload}")

    logging.info("Posted to Facebook successfully: %s", payload)
    return payload


# -----------------------------------------------------------------------------
# Scheduling
# -----------------------------------------------------------------------------

def _scheduled_post_worker(
    job: Dict[str, Any],
    data: Dict[str, Any],
    page_id: str,
    page_access_token: str,
    state_path: Path,
) -> None:
    job_id = job["job_id"]
    try:
        with STATE_LOCK:
            state = load_state(state_path)
            current = get_job_by_id(state, job_id)
            if current and current.get("status") == "posted":
                logging.info("Skipping already posted job: %s", job_id)
                return

        image_path = job["image_path"]
        if job.get("regenerate_image"):
            image_path = generate_poster(data, output_path=image_path, variation=job.get("variation"))

        result = post_to_facebook(
            page_id=page_id,
            page_access_token=page_access_token,
            image_path=image_path,
            caption=job["caption"],
        )

        with STATE_LOCK:
            state = load_state(state_path)
            current = get_job_by_id(state, job_id) or job
            current["status"] = "posted"
            current["posted_at"] = datetime.now().isoformat()
            current["facebook_response"] = result
            upsert_job(state, current)
            add_used_caption_hash(state, job["caption_hash"])
            save_state(state, state_path)

        logging.info("Scheduled post completed: %s", job_id)

    except Exception as exc:  # noqa: BLE001
        logging.exception("Scheduled post failed for %s: %s", job_id, exc)
        with STATE_LOCK:
            state = load_state(state_path)
            current = get_job_by_id(state, job_id) or job
            current["status"] = "failed"
            current["last_error"] = str(exc)
            current["last_attempt_at"] = datetime.now().isoformat()
            upsert_job(state, current)
            save_state(state, state_path)


def schedule_posts(
    data: Dict[str, Any],
    page_id: str,
    page_access_token: str,
    base_image_path: str,
    state_path: str = str(STATE_FILE),
) -> List[threading.Timer]:
    timers: List[threading.Timer] = []
    state_file = Path(state_path)
    now = datetime.now()
    movie_key = normalize_movie_key(MovieData(**data))

    with STATE_LOCK:
        state = load_state(state_file)
        used_hashes = get_used_caption_hashes(state)

    for day_offset in range(1, 4):
        target_day = date.today() + timedelta(days=day_offset)
        slot_times = [dtime(hour=9, minute=0), dtime(hour=21, minute=0)]

        for slot_index, slot_time in enumerate(slot_times, start=1):
            run_at = datetime.combine(target_day, slot_time)
            if run_at <= now:
                continue

            job_id = f"{movie_key}:{run_at.strftime('%Y%m%d%H%M')}"

            with STATE_LOCK:
                state = load_state(state_file)
                existing = get_job_by_id(state, job_id)
                if existing and existing.get("status") in {"pending", "posted"}:
                    logging.info("Job already exists, skipping creation: %s", job_id)
                    continue
                used_hashes = get_used_caption_hashes(state)

            caption = generate_caption(data, used_caption_hashes=used_hashes)
            caption_hash = _caption_hash(caption)

            regenerate_image = False
            variation = f"day-{day_offset}-slot-{slot_index}"
            image_path = base_image_path if not regenerate_image else f"poster_{job_id}.png"

            job = {
                "job_id": job_id,
                "movie_key": movie_key,
                "run_at": run_at.isoformat(),
                "status": "pending",
                "caption": caption,
                "caption_hash": caption_hash,
                "image_path": image_path,
                "regenerate_image": regenerate_image,
                "variation": variation,
                "created_at": datetime.now().isoformat(),
            }

            with STATE_LOCK:
                state = load_state(state_file)
                upsert_job(state, job)
                add_used_caption_hash(state, caption_hash)
                save_state(state, state_file)

            delay_seconds = max((run_at - datetime.now()).total_seconds(), 1.0)
            timer = threading.Timer(
                delay_seconds,
                _scheduled_post_worker,
                args=(job, data, page_id, page_access_token, state_file),
            )
            timer.daemon = False
            timer.start()
            timers.append(timer)

            logging.info("Scheduled job %s at %s (in %.1f sec)", job_id, run_at.isoformat(), delay_seconds)

    return timers


# -----------------------------------------------------------------------------
# CLI and main workflow
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automated movie promotion poster + Facebook posting system.")
    parser.add_argument("--movie_name", required=True)
    parser.add_argument("--hero_name", required=True)
    parser.add_argument("--heroine_name", required=True)
    parser.add_argument("--director_name", required=True)
    parser.add_argument("--genre", required=True)
    parser.add_argument("--release_date", required=False)
    parser.add_argument("--requirements_poster", required=False)
    return parser.parse_args()


def main() -> None:
    setup_logging()
    load_dotenv_file()

    args = parse_args()
    movie = MovieData(
        movie_name=args.movie_name,
        hero_name=args.hero_name,
        heroine_name=args.heroine_name,
        director_name=args.director_name,
        genre=args.genre,
        release_date=args.release_date,
        requirements_poster=args.requirements_poster,
    )

    validate_inputs(movie)

    credentials = load_page_credentials()
    page_id = credentials["page_id"]
    page_access_token = credentials["page_access_token"]

    movie_data = asdict(movie)

    poster_path = generate_poster(movie_data, output_path=str(DEFAULT_POSTER_PATH))

    with STATE_LOCK:
        state = load_state(STATE_FILE)
        used_hashes = get_used_caption_hashes(state)

    immediate_caption = generate_caption(movie_data, used_caption_hashes=used_hashes)
    immediate_hash = _caption_hash(immediate_caption)

    result = post_to_facebook(
        page_id=page_id,
        page_access_token=page_access_token,
        image_path=poster_path,
        caption=immediate_caption,
    )

    with STATE_LOCK:
        state = load_state(STATE_FILE)
        add_used_caption_hash(state, immediate_hash)
        state.setdefault("immediate_posts", []).append(
            {
                "movie_key": normalize_movie_key(movie),
                "posted_at": datetime.now().isoformat(),
                "caption_hash": immediate_hash,
                "image_path": poster_path,
                "facebook_response": result,
            }
        )
        save_state(state, STATE_FILE)

    logging.info("Immediate promo post published. No schedules were created.")


if __name__ == "__main__":
    main()
