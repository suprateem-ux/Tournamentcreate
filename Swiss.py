import requests
from datetime import datetime, timedelta
import pytz
import os
from datetime import timezone

API_TOKEN = os.getenv("LICHESS_TOKEN")
TEAM_ID = "international-chess-talent"
API_URL = "https://lichess.org/api/tournament"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

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
    ("11:30 PM", 3, 2, 8)
]

def ist_to_utc_timestamp(ist_time_str):
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    time_obj = datetime.strptime(ist_time_str, "%I:%M %p").time()
    combined = datetime.combine(now.date(), time_obj)
    combined = ist.localize(combined)
    if combined < now:
        combined += timedelta(days=1)
    utc_time = combined.astimezone(pytz.utc)
    return int(utc_time.timestamp() * 1000), combined

def get_tournament_name(index, time_str, base, inc, rounds):
    prefix = "GCT" if time_str == "2:00 PM" else "GS" if time_str >= "3:30 PM" else "FPT"
    today = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%b%d")
    return f"{prefix} {base}+{inc} {rounds}R {today} {index+1}"

def create_tournament(name, start_time, base, increment, rounds):
    utc_timestamp, ist_datetime = ist_to_utc_timestamp(start_time)
    print(f"🛠 Trying to create tournament for {ist_datetime.strftime('%I:%M %p')} IST...")

    payload = {
        "name": name,
        "clockTime": base,
        "clockIncrement": increment,
        "minutes": 720,
        "startDate": utc_timestamp,
        "variant": "standard",
        "rated": "true",
        "nbRounds": rounds,
        "tournamentType": "swiss",
        "teamId": TEAM_ID
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=payload)
        if response.status_code == 200:
            print(f"✅ Created: {name}")
        else:
            print(f"❌ Failed: {name} | {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error while creating tournament: {e}")

def main():
    now_utc = datetime.now(timezone.utc)
    for idx, (time_str, base, inc, rounds) in enumerate(TOURNAMENTS):
        utc_millis, tournament_time = ist_to_utc_timestamp(time_str)
        utc_dt = datetime.fromtimestamp(utc_millis / 1000, tz=timezone.utc)
        # Only create if tournament is within 15 minutes in future
        if 0 <= (utc_dt - now_utc).total_seconds() < 900:
            name = get_tournament_name(idx, time_str, base, inc, rounds)
            create_tournament(name, time_str, base, inc, rounds)
            break

if __name__ == "__main__":
    main()
