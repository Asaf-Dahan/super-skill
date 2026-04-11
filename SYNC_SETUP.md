# Sync Setup -- Keeping Your Super Skills Current

super-skill-sync is a script that runs automatically to keep all
your Super Skills up to date. It does three things in one command:

  1. Pulls the latest changes from GitHub for each Super Skill
  2. Checks the sources you monitor for changes (drift detection)
  3. Regenerates SUMMARY.md for each Super Skill

Run it manually any time, or set it up to run on a schedule.

---

## Step 1: Register Your Super Skills

Open this file in any text editor:

  scripts/super-skill-sync.py

Find the REGISTRY section near the top. It looks like this:

  REGISTRY = [
      {
          "name": "stack-os",
          "path": "~/super-skill-stack-os",
          "monitor_urls": [
              "https://example.com/changelog",
          ],
      },
  ]

Replace the example entry with your own Super Skill.
Add one entry per Super Skill you have created.

### Fields

name
  A short label for this Super Skill.
  Use the same name as your folder, without "super-skill-".
  Example: if your folder is super-skill-garden, use "garden"

path
  The full path to your Super Skill folder on your computer.
  Windows example: C:/Users/YourName/super-skills/super-skill-garden
  Mac example: ~/super-skills/super-skill-garden
  Use forward slashes on all systems.

monitor_urls
  A list of web pages to check for changes.
  These should be changelog or release pages for tools you use.
  If a page returns an error, the script writes a drift alert
  to PENDING.md for your review.
  You can leave this list empty if you do not want drift checking.

### Example with two Super Skills

  REGISTRY = [
      {
          "name": "garden",
          "path": "~/super-skills/super-skill-garden",
          "monitor_urls": [
              "https://www.rhs.org.uk/about-the-rhs/publications/",
          ],
      },
      {
          "name": "investments",
          "path": "~/super-skills/super-skill-investments",
          "monitor_urls": [
              "https://www.sec.gov/rss/rss_edgar_latest.xml",
          ],
      },
  ]

---

## Step 2: Run the Script

Open a terminal in your super-skill folder and run:

  python scripts/super-skill-sync.py

The script will:
  - Pull latest changes for each registered Super Skill
  - Check each monitor URL
  - Regenerate SUMMARY.md for each Super Skill
  - Print a summary of what happened

To also push updates to NotebookLM after syncing:

  python scripts/super-skill-sync.py --feed

To see what would happen without making any changes:

  python scripts/super-skill-sync.py --dry-run

---

## Step 3: Set Up a Schedule (Optional)

You can set the sync script to run automatically on a schedule
so you never need to think about it.

### Windows -- Task Scheduler

1. Open Task Scheduler (search for it in the Start menu)
2. Click "Create Basic Task"
3. Name it: Super Skill Sync
4. Set the trigger: Weekly, on a day you choose
5. Set the action: Start a program
6. Program: python
7. Arguments: C:\path\to\super-skill\scripts\super-skill-sync.py
8. Start in: C:\path\to\super-skill
9. Click Finish

### Mac -- cron

Open Terminal and run:

  crontab -e

Add this line to run every Sunday at 9am:

  0 9 * * 0 python3 ~/super-skills/super-skill/scripts/super-skill-sync.py

Save and exit. The script will run automatically each week.

### How often to run

Daily: if your domain changes fast (stock prices, active development)
Weekly: for most domains (tools, services, professional knowledge)
Monthly: for slow-moving domains (regulations, long-term strategy)

---

## What Happens When Drift Is Detected

If a monitored URL returns an error or unexpected response, the
script writes a drift alert to PENDING.md in that Super Skill.

The alert looks like this:

  ## DRIFT-001: [skill-name] - [domain]
  Date detected: [date]
  Type: DRIFT DETECTED
  Status: AWAITING REVIEW

  Source URL returned unexpected status.
  Manual review required at: [URL]

Open Claude Code on that Super Skill folder and run /ss-pending
to review and decide what to do.

---

## Troubleshooting

Script not found:
  Make sure you are running the command from inside the
  super-skill folder, not from inside a Super Skill folder.

Path not found error:
  Check that the path in REGISTRY matches the actual folder
  location on your computer. Use forward slashes on Windows too.

Git pull failed:
  Make sure your Super Skill folder is connected to GitHub.
  Run: git remote -v
  If it shows nothing, connect it using Prompt 0 in ONBOARDING.md.

Python not found:
  On Windows try: py scripts/super-skill-sync.py
  On Mac try: python scripts/super-skill-sync.py

---

*Super Skill v2.7.1 -- April 2026*
*github.com/Asaf-Dahan/super-skill*
