import json

def log(event_data: dict):
    with open("messages.log", "a", encoding="utf-8") as file:
        timestamp = event_data["timestamp"]
        username = event_data["author"]["username"]
        channel_id = event_data["channel_id"]
        content = event_data["content"]
        message_log = f"[{timestamp}] - {username} at {channel_id}: {content}\n"
        file.write(message_log)

def ident_data(token: str, client: dict) -> dict:
    return json.dumps({
        "op": 2,
        "d": {
            "token": token,
            "capabilities": 30717,
            "properties": {
                "os": client.get("os"),
                "browser": client.get("browser"),
                "device": "",
                "system_locale": "en-US",
                "browser_user_agent": client.get("user_agent"),
                "browser_version": "133.0",
                "os_version": "",
                "referrer": "https://www.google.com/",
                "referring_domain": "www.google.com",
                "search_engine": "google",
                "referrer_current": "",
                "referring_domain_current": "",
                "release_channel": "stable",
                "client_build_number": 359691,
                "client_event_source": None,
                "has_client_mods": False,
            },
            "presence": {
                "status": "unknown",
                "since": 0,
                "activities": [],
                "afk": False,
            },
            "compress": False,
            "client_state": {"guild_versions": {}},
        },
    })
