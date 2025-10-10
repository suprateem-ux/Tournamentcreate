import requests, datetime, os, pathlib
TOKEN   = os.environ["LICHESS_KEY"].strip('"')
TEAM    = "international-chess-talent"
ROUNDS  = 7
CLOCK   = 180      
NUM_TMT = 12
GAP_HRS = 2
headers = {"Authorization": f"Bearer {TOKEN}"}
url     = f"https://lichess.org/api/swiss/new/{TEAM}"
DESC_FILE = pathlib.Path(__file__).with_name("description.txt")
try:
    with DESC_FILE.open(encoding="utf-8") as f:
        LONG_DESC = f.read().strip()
except FileNotFoundError:
    raise SystemExit("❌ description.txt not found!")
def create_one(idx: int, start_time: datetime.datetime) -> None:
    name = "Grand Swiss Tournament"[:30]
    payload = {
        "name":            name,
        "clock.limit":     CLOCK,
        "clock.increment": 0,
        "startsAt":        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nbRounds":        ROUNDS,
        "interval":        15,
        "variant":         "standard",
        "rated":           "true",
        "description":     LONG_DESC,
    }
    r = requests.post(url, headers=headers, data=payload)
    if r.status_code == 200:
        try:
            data = r.json()
            if 'id' in data:
                print(f" Tmt #{idx+1} created successfully. ID: {data['id']}")
            else:
                print(f"  Tmt #{idx+1} created (200 OK) but no ID in response:", data)
        except ValueError:
            print(f"  Tmt #{idx+1} created (200 OK) but response is not JSON:", r.text)
    else:
        print(f" oh no  Tmt #{idx+1} error. Status code: {r.status_code}")
        print("Response text:", r.text)
if __name__ == "__main__":
    first_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    for i in range(NUM_TMT):
        start = first_start + datetime.timedelta(hours=i * GAP_HRS)
        create_one(i, start)
