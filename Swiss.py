#!/usr/bin/env python3
import requests
import random
import os

TEAM_ID = "darkonswiss-dos"
API_TOKEN = os.environ["KEY"]  # put your lichess personal API token here

# Define tournament options
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
    return "Welcome to our Swiss tournament!"

def create_swiss():
    option = random.choice(OPTIONS)
    description = read_description()

    payload = {
        "name": option["name"],
        "clock.limit": option["clock"]["limit"],
        "clock.increment": option["clock"]["increment"],
        "nbRounds": option["nbRounds"],
        "rated": True,
        "description": description,
    }

    url = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    print(f"Creating tournament: {payload['name']} "
          f"({payload['clock.limit']//60}+{payload['clock.increment']}, "
          f"{payload['nbRounds']} rounds)")

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        print("Tournament created successfully!")
        print(r.json())
    else:
        print("Error:", r.status_code, r.text)


if __name__ == "__main__":
    create_swiss()
