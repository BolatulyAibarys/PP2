import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    default_settings = {
        "sound": True,
        "car_color": "green",
        "difficulty": "normal"
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)

        for key in default_settings:
            if key not in settings:
                settings[key] = default_settings[key]

        return settings

    except Exception:
        save_settings(default_settings)
        return default_settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_score(username, score, coins, distance):
    data = load_leaderboard()

    data.append({
        "username": username,
        "score": score,
        "coins": coins,
        "distance": distance
    })

    data.sort(key=lambda item: item["score"], reverse=True)

    data = data[:10]

    save_leaderboard(data)