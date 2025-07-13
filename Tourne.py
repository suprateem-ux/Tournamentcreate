import requests
from datetime import datetime, timedelta
import pytz
import os
import time

# ✅ Secure API token from GitHub Secrets (env variable)
API_TOKEN = os.getenv("LICHESS_TOKEN")
TEAM_ID = "international-chess-talent"
API_URL = "https://lichess.org/api/tournament"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# ✅ Daily Swiss tournament schedule (IST)
TOURNAMENTS = [
    ("2:00 PM", 7, 2, 5),     # Grand Chess Tournament (3rd set)
    ("3:30 PM", 7, 2, 6),     # Grand Swiss (2nd set)
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
    ("11:30 PM", 3, 2, 8)
]

# ✅ Convert IST to UTC in millis for Lichess
def ist_to_utc_timestamp(ist_time_str):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    time_obj = datetime.strptime(ist_time_str, "%I:%M %p").time()
    combined = datetime.combine(now.date(), time_obj)
    combined = ist.localize(combined)
    if combined < now:
        combined += timedelta(days=1)
    utc_time = combined.astimezone(pytz.utc)
    return int(utc_time.timestamp() * 1000)

# ✅ Safe tournament name under 30 characters with valid characters
def get_tournament_name(index, time_str, base, inc, rounds):
    if time_str == "2:00 PM":
        prefix = "GCT"  # Grand Chess Tournament
    elif time_str >= "3:30 PM":
        prefix = "GS"   # Grand Swiss
    else:
        prefix = "FPT"  # Free Practice Tournament
    today = datetime.now().strftime("%b%d")
    return f"{prefix} {base}+{inc} {rounds}R {today} {index+1}"

# ✅ Create tournament via API
def create_tournament(name, start_time, base, increment, rounds):
    payload = {
        "name": name,
        "clockTime": base,
        "clockIncrement": increment,
        "minutes": 720,  # buffer time per round
        "startDate": ist_to_utc_timestamp(start_time),
        "variant": "standard",
        "rated": "true",
        "nbRounds": rounds,
        "tournamentType": "swiss",
        "teamId": TEAM_ID
    }

    response = requests.post(API_URL, headers=HEADERS, data=payload)

    if response.status_code == 200:
        print(f"✅ Created: {name}")
    else:
        print(f"❌ Failed: {name} | {response.status_code} - {response.text}")

# ✅ Loop through all tournament entries
 # ⏱️ required for sleep()
def main():
    for idx, (time_str, base, inc, rounds) in enumerate(TOURNAMENTS):
        name = get_tournament_name(idx, time_str, base, inc, rounds)
        create_tournament(name, time_str, base, inc, rounds)
        if idx != len(TOURNAMENTS) - 1:
            print("⏳ Waiting 15 minutes before next tournament...")
            time.sleep(15 * 60)  # wait 900 seconds = 15 minutes

if __name__ == "__main__":
    main()
