name: Run Swiss Tournament Hourly

# Trigger workflow every hour
on:
  schedule:
    - cron: '0 * * * *'   # At minute 0 of every hour
  workflow_dispatch:       # Allow manual trigger too

jobs:
  run-swiss:
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ Checkout repo
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2️⃣ Set up Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11   # or 3.x of your choice

      # 3️⃣ Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      # 4️⃣ Run the Swiss script
      - name: Run swiss.py
        run: python Swiss.py
        env:
          KEY: ${{ secrets.KEY }}   # Your Lichess API token
