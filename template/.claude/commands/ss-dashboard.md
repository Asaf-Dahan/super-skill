# /ss-dashboard

Generates the Super Skill Dashboard.

## What it does

Scans for Super Skills in the current directory or parent directory.
Runs cross-layer analysis on each selected Super Skill.
Computes Health Score, insights, and activity trends.
Saves a snapshot to wiki/dashboard_history.json.
Generates wiki/dashboard.html and opens it in the default browser.

## Usage

/ss-dashboard

No arguments required. If multiple Super Skills are found,
the script will ask which ones to include.

## Command

Run:
python scripts/generate_dashboard.py

Then open wiki/dashboard.html in your browser.

## Output files

wiki/dashboard.html         the dashboard (gitignored -- contains your domain data)
wiki/dashboard_history.json health score history (gitignored -- contains your domain data)
