import requests
from datetime import datetime, timedelta, timezone
import pytz
import os
import pathlib
import json

# === Config ===
API_TOKEN = os.environ["KEY"]
TEAM_ID = "international-chess-talent"
DESC_FILE = pathlib.Path(__file__).with_name("description.txt")

# === Load Description ===
try:
    with DESC_FILE.open(encoding="utf-8") as f:
        DESCRIPTION = f.read().strip()
except FileNotFoundError:
    raise SystemExit("❌ description.txt not found!")

# === API Setup ===
API_URL = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# ✅ Full Daily Schedule (IST)
TOURNAMENTS = [
    ("2:00 PM", 7, 2, 5),
    ("3:30 PM", 7, 2, 6),
    ("4:30 PM", 5, 2, 8),
    ("5:00 PM", 5, 0, 8),
    ("5:00 PM", 10, 0, 8),
    ("5:30 PM", 3, 2, 8),
    ("6:00 PM", 10, 0, 6),
    ("6:30 PM", 5, 1, 6),
    ("6:30 PM", 7, 2, 6),
    ("8:00 PM", 10, 0, 6),
    ("8:30 PM", 3, 2, 6),
    ("9:00 PM", 5, 0, 8),
    ("9:30 PM", 3, 2, 8),
    ("10:30 PM", 5, 2, 8),
    ("11:30 PM", 3, 2, 8),
]

def ist_to_utc_start_str(ist_time_str):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    time_obj = datetime.strptime(ist_time_str, "%I:%M %p").time()
    start_dt = datetime.combine(now.date(), time_obj)
    start_dt = ist.localize(start_dt)

    if start_dt < now:
        start_dt += timedelta(days=1)

    return start_dt.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def create_tournament(name, start_time_str, base, inc, rounds):
    start_iso = ist_to_utc_start_str(start_time_str)
    print(f"🛠 Creating '{name}' for start at {start_iso}")

    payload = {
        "name": name[:30],
        "clock.limit": base * 60,
        "clock.increment": inc,
        "startsAt": start_iso,
        "nbRounds": rounds,
        "variant": "standard",
        "rated": "True",
        "description": DESCRIPTION,
        "interval": 15,
       # "teamId": TEAM_ID
    }

    r = requests.post(API_URL, headers=HEADERS, data=payload)
    if r.status_code == 200:
        response_data = r.json()
        print(f"✅ Created: {response_data.get('id')} @ {response_data.get('startsAt')}")
        print(json.dumps(response_data, indent=2))
    else:
        try:
            print("❌ Error:")
            print(json.dumps(r.json(), indent=2))
        except Exception:
            print(f"❌ Failed: {r.status_code} - {r.text}")

def main():
    now_utc = datetime.now(timezone.utc)
    for idx, (time_str, base, inc, rounds) in enumerate(TOURNAMENTS):
        start_iso = ist_to_utc_start_str(time_str)
        start_dt = datetime.strptime(start_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

        # If the tournament is due within the next 15 minutes
        if 0 <= (start_dt - now_utc).total_seconds() < 900:
            name = f"{base}+{inc} {rounds}R {time_str} T{idx+1}"
            create_tournament(name, time_str, base, inc, rounds)
            break  # Only one tournament per run

if __name__ == "__main__":
    main()
