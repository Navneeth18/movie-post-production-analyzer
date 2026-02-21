import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

GRAPH_BASE_URL = "https://graph.facebook.com/v19.0"


def pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def exchange_for_long_lived_user_token(app_id: str, app_secret: str, short_lived_user_token: str) -> str:
    url = f"{GRAPH_BASE_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_user_token,
    }
    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if not response.ok or "access_token" not in data:
        raise RuntimeError(f"Failed token exchange: {pretty(data)}")

    return data["access_token"]


def get_page_access_token(page_id: str, long_lived_user_token: str) -> str:
    url = f"{GRAPH_BASE_URL}/{page_id}"
    params = {
        "fields": "id,name,access_token",
        "access_token": long_lived_user_token,
    }
    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if not response.ok or "access_token" not in data:
        raise RuntimeError(f"Failed fetching page token: {pretty(data)}")

    print(f"Page resolved: {data.get('name')} ({data.get('id')})")
    return data["access_token"]


def debug_token(input_token: str, app_id: str, app_secret: str) -> Dict[str, Any]:
    app_token = f"{app_id}|{app_secret}"
    url = f"{GRAPH_BASE_URL}/debug_token"
    params = {
        "input_token": input_token,
        "access_token": app_token,
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    if not response.ok or "data" not in data:
        raise RuntimeError(f"Failed token debug: {pretty(data)}")

    return data["data"]


def format_unix_ts(unix_ts: Optional[int]) -> str:
    if not unix_ts:
        return "N/A"
    dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    return dt.isoformat()


def main() -> None:
    print("=== Facebook Long-Lived Page Token Helper ===")
    print("You need a short-lived USER token with pages_manage_posts + pages_show_list permissions.\n")

    app_id = input("App ID: ").strip()
    app_secret = input("App Secret: ").strip()
    short_user_token = input("Short-lived User Access Token: ").strip()
    page_id = input("Page ID: ").strip()

    if not all([app_id, app_secret, short_user_token, page_id]):
        print("All fields are required.")
        sys.exit(1)

    try:
        long_user_token = exchange_for_long_lived_user_token(app_id, app_secret, short_user_token)
        print("\nLong-lived USER token generated successfully.\n")

        page_token = get_page_access_token(page_id, long_user_token)
        print("Page access token generated successfully.\n")

        token_info = debug_token(page_token, app_id, app_secret)
        print("=== Page Token Debug Info ===")
        print(f"Valid: {token_info.get('is_valid')}")
        print(f"App ID: {token_info.get('app_id')}")
        print(f"Type: {token_info.get('type')}")
        print(f"Expires At (UTC): {format_unix_ts(token_info.get('expires_at'))}")
        print(f"Scopes: {token_info.get('scopes')}\n")

        print("=== Copy into config.json ===")
        print(f"page_id: {page_id}")
        print(f"page_access_token: {page_token}")

    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
