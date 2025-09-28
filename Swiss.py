#!/usr/bin/env python3
import requests
import random
import os
import sys

TEAM_ID = "darkonswiss-dos"

# Get API token from environment
API_TOKEN = os.environ.get("KEY")
if not API_TOKEN:
    sys.exit("Error: API token not found. Please set KEY environment variable.")

# Define Swiss formats
OPTIONS = [
    {"name": "DOS BLIZ SWISS",  "clock": {"limit": 180,  "increment": 0}, "nbRounds": 11},   # 3+0
    {"name": "DOS RAPID SWISS", "clock": {"limit": 600,  "increment": 0}, "nbRounds": 9},    # 10+0
    {"name": "DOS BULLET SWISS","clock": {"limit": 60,   "increment": 0}, "nbRounds": 20},   # 1+0
    {"name": "DOS BULLET SWISS","clock": {"limit": 120,  "increment": 1}, "nbRounds": 15},   # 2+1
]

def read_description():
    path = os.path.join(os.path.dirname(__file__), "description.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "This team offers hourly swisses!"

def create_swiss():
    # Pick a random format
    option = random.choice(OPTIONS)
    description = read_description()

    # Prepare payload for form submission
    payload = {
        "name": option["name"],
        "clock[limit]": option["clock"]["limit"],
        "clock[increment]": option["clock"]["increment"],
        "nbRounds": option["nbRounds"],
        "rated": "true",            # form requires string
        "description": description,
    }

    print(f"Creating tournament: {option['name']} ({option['clock']['limit']//60}+{option['clock']['increment']}, {option['nbRounds']} rounds)")

    url = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        data = r.json()
        print("✅ Tournament created successfully!")
        print("Name:", data.get("name"))
        print("ID:", data.get("id"))
        print("Rounds:", data.get("nbRounds"))
        print("Clock:", f"{data['clock']['limit']//60}+{data['clock']['increment']}")
        print("Rated:", data.get("rated"))
        print("URL:", f"https://lichess.org/swiss/{data.get('id')}")
    else:
        print("❌ Error:", r.status_code, r.text)

if __name__ == "__main__":
    create_swiss()
