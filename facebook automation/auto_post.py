import json
import logging
import sys
import time
from typing import Any, Dict, Optional, Tuple

import requests

GRAPH_BASE_URL = "https://graph.facebook.com/v19.0"
CONFIG_FILE = "config.json"
LOG_FILE = "autopost.log"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_root_keys = {"page_id", "page_access_token", "posts"}
    missing = required_root_keys.difference(data.keys())
    if missing:
        raise ValueError(f"Missing required config keys: {sorted(missing)}")

    if not isinstance(data["posts"], list):
        raise ValueError("'posts' must be a list")

    for idx, post in enumerate(data["posts"], start=1):
        if "message" not in post:
            raise ValueError(f"Post #{idx} missing required field: message")

    return data


def _request_with_retry(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 20,
    max_retries: int = 3,
) -> requests.Response:
    delay_seconds = 2
    last_exception: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.request(method, url, params=params, data=data, timeout=timeout)
            if response.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
                logging.warning(
                    "Transient HTTP %s from %s. Retry %s/%s in %ss",
                    response.status_code,
                    url,
                    attempt,
                    max_retries,
                    delay_seconds,
                )
                time.sleep(delay_seconds)
                delay_seconds *= 2
                continue
            return response
        except requests.RequestException as exc:
            last_exception = exc
            if attempt < max_retries:
                logging.warning(
                    "Network error on attempt %s/%s: %s. Retrying in %ss",
                    attempt,
                    max_retries,
                    exc,
                    delay_seconds,
                )
                time.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                break

    raise RuntimeError(f"Request failed after {max_retries} attempts: {last_exception}")


def parse_graph_error(response_json: Dict[str, Any]) -> Tuple[Optional[int], str]:
    error = response_json.get("error", {})
    code = error.get("code")
    message = error.get("message", "Unknown Graph API error")
    return code, message


def validate_page_access_token(page_id: str, access_token: str) -> bool:
    url = f"{GRAPH_BASE_URL}/{page_id}"
    params = {
        "fields": "id,name",
        "access_token": access_token,
    }

    try:
        response = _request_with_retry("GET", url, params=params)
        response_json = response.json()
    except Exception as exc:  # noqa: BLE001
        logging.error("Token validation request failed: %s", exc)
        return False

    if response.ok and "id" in response_json:
        logging.info("Token validation successful for page '%s' (%s)", response_json.get("name"), page_id)
        return True

    code, msg = parse_graph_error(response_json)
    if code == 190:
        logging.error("Token is invalid or expired (code 190): %s", msg)
    elif code in (10, 200):
        logging.error(
            "Permission error validating token (code %s): %s. "
            "This can happen even when posting permissions are present.",
            code,
            msg,
        )
    else:
        logging.error("Token validation failed: %s", response_json)

    return False


def _upload_unpublished_photo(page_id: str, access_token: str, image_url: str) -> str:
    url = f"{GRAPH_BASE_URL}/{page_id}/photos"
    payload = {
        "url": image_url,
        "published": "false",
        "access_token": access_token,
    }

    response = _request_with_retry("POST", url, data=payload)
    response_json = response.json()

    if not response.ok or "id" not in response_json:
        code, msg = parse_graph_error(response_json)
        raise RuntimeError(f"Image upload failed (code={code}): {msg}")

    return response_json["id"]


def post_to_facebook(
    page_id: str,
    access_token: str,
    message: str,
    image_url: Optional[str] = None,
    link_url: Optional[str] = None,
) -> Dict[str, Any]:
    feed_url = f"{GRAPH_BASE_URL}/{page_id}/feed"
    payload: Dict[str, Any] = {
        "message": message,
        "access_token": access_token,
    }

    if link_url:
        payload["link"] = link_url

    if image_url:
        media_fbid = _upload_unpublished_photo(page_id, access_token, image_url)
        payload["attached_media[0]"] = json.dumps({"media_fbid": media_fbid})

    response = _request_with_retry("POST", feed_url, data=payload)

    try:
        response_json = response.json()
    except ValueError:
        response_json = {"raw_text": response.text}

    if response.ok and "id" in response_json:
        logging.info("Post success: %s", response_json)
        return {"success": True, "response": response_json}

    code, msg = parse_graph_error(response_json)
    if code == 190:
        logging.error("Post failed: token expired/invalid (code 190): %s", msg)
    elif code in (10, 200):
        logging.error("Post failed: missing permissions (code %s): %s", code, msg)
    else:
        logging.error("Post failed: %s", response_json)

    return {"success": False, "response": response_json}


def main() -> None:
    setup_logging()
    logging.error(
        "auto_post.py is disabled to prevent accidental static-post publishing. "
        "Use movie_promo_auto_post.py for generated image + generated content posts."
    )
    sys.exit(1)

    try:
        cfg = load_config(CONFIG_FILE)
    except Exception as exc:  # noqa: BLE001
        logging.error("Failed loading config '%s': %s", CONFIG_FILE, exc)
        sys.exit(1)

    page_id = cfg["page_id"]
    access_token = cfg["page_access_token"]
    posts = cfg["posts"]

    if not validate_page_access_token(page_id, access_token):
        logging.warning(
            "Startup validation could not confirm read permissions. "
            "Continuing anyway; immediate post attempts will still be made."
        )

    if not posts:
        logging.warning("No posts found in config. Nothing to publish.")
        return

    post = posts[0]
    logging.info("Publishing only the first post immediately")
    result = post_to_facebook(
        page_id=page_id,
        access_token=access_token,
        message=post["message"],
        image_url=post.get("image_url"),
        link_url=post.get("link_url"),
    )
    status = "SUCCESS" if result["success"] else "FAILURE"
    logging.info("Immediate first-post result: %s | payload=%s", status, result["response"])

    logging.info("Run complete. No schedules were created.")


if __name__ == "__main__":
    main()
