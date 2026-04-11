# Claude Code Channels -- Mobile Access for Super Skill

## What This Is

Claude Code Channels lets you send commands to a running Claude Code
session from your phone via Telegram or Discord. For Super Skill users,
this means you can review PENDING items, trigger drift checks, run
/ss-sync, and approve or reject proposals -- all from your mobile device,
without opening a laptop. Your Super Skill session stays alive on your
machine inside tmux. Channels is the remote control.

---

## Prerequisites

Before setting up Channels you need three things:

- **Claude Code installed and a Super Skill activated.**
  If you have not activated a Super Skill yet, follow README.md first.

- **A Telegram account** (or Discord account).
  Telegram is the recommended path. Download it from https://telegram.org
  if you do not have it.

- **tmux installed.**
  tmux is a terminal multiplexer. It keeps your Claude Code session running
  even when you close the terminal window or disconnect from SSH. Without
  tmux, closing the terminal kills the session and Channels stops working.

  Install tmux:

  Mac:
    brew install tmux

  Linux (Debian/Ubuntu):
    sudo apt install tmux

  Linux (Fedora/RHEL):
    sudo dnf install tmux

  Windows:
    tmux does not run natively on Windows. Use WSL (Windows Subsystem for
    Linux) instead:
      1. Open PowerShell as Administrator
      2. Run: wsl --install
      3. Restart your computer when prompted
      4. Open the WSL terminal and run: sudo apt install tmux
    All tmux and Claude Code commands below run inside the WSL terminal.

---

## Setup: Step by Step

### Step 1 -- Start a persistent tmux session

Open your terminal (or WSL terminal on Windows) and run:

```bash
tmux new -s superskill
```

This creates a named tmux session called "superskill". Everything you run
inside this session survives terminal disconnects.

To reconnect to the session later (after closing the terminal or SSH):

```bash
tmux attach -t superskill
```

Why this matters: if the terminal that started Claude Code closes, the
Claude Code process dies and Channels stops responding. tmux prevents this
by keeping the process alive in the background.

### Step 2 -- Start Claude Code with Channels enabled

Inside the tmux session, navigate to your Super Skill folder and start
Claude Code with the --channels flag:

```bash
cd ~/super-skills/super-skill-yourdomain
claude --channels .
```

The --channels flag tells Claude Code to listen for incoming messages
from connected messaging platforms. Without this flag, Channels commands
sent from Telegram are ignored.

### Step 3 -- Connect Telegram

1. Open Telegram on your phone or desktop.

2. Search for @BotFather and start a conversation.

3. Send the command:
     /newbot

4. BotFather will ask for a name. Choose anything you like.
   Example: "My Super Skill Bot"

5. BotFather will ask for a username. It must end in "bot".
   Example: "my_superskill_bot"

6. BotFather will reply with a token. It looks like:
     1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   Copy this token.

7. In your Claude Code terminal (inside tmux), type:
     /telegram:configure

8. Paste the token when prompted.

9. Claude Code will display a pairing code (a short alphanumeric string).

10. Go back to Telegram. Open a conversation with your new bot
    (search for the username you chose in step 5).

11. Send the pairing code as a message to the bot.

12. Claude Code will confirm: "Telegram connected."

### Step 4 -- Test the connection

From Telegram, send this message to your bot:

    /ss-pending

You should receive a reply listing all open PENDING items in your
Super Skill (or "Queue clear" if nothing is pending).

If you get no response, see Troubleshooting below.

---

## Supported Commands via Channels

These slash commands work when sent from Telegram to your connected bot:

| Command | What it does via mobile |
|---------|------------------------|
| /ss-pending | Lists all open PENDING items with age and type |
| /ss-drift | Checks monitored sources for changes |
| /ss-sync | Pulls all Super Skills and checks drift |
| /ss-council | Shows active expert debates and challenges |
| /ss-summary | Returns the current SUMMARY.md content |
| /ss-channels | Shows Channels connection status |

All commands are read-only by default. They report status but do not
modify any layer file. The one exception is the approval flow described
below.

---

## Approving PENDING Items via Mobile

You can review and approve PENDING items directly from Telegram.

### Step 1: Request the pending list

Send:
    /ss-pending

The bot replies with each open item: ID, title, date added, days waiting,
and recommended action.

### Step 2: Review the item

Read the summary. If you need more context, send:
    Tell me more about PENDING-003

The agent will read the full PENDING entry and any referenced layer files,
then summarize the context.

### Step 3: Approve, reject, or defer

Send one of:
    Approve PENDING-003
    Reject PENDING-003 -- reason: not needed at this time
    Defer PENDING-003

The agent will:
1. Execute the approval action (move content to the correct layer file,
   or move to the Resolved section for rejections)
2. Write a LOG entry with source: channels
3. Run update_summary.py to keep SUMMARY.md current
4. Confirm the action back to you in Telegram

Every approval, rejection, or deferral made via Channels is recorded in
LOG.md with this format:

    ### LOG-NNN: [item title]
    Date: YYYY-MM-DD
    Action: approved | rejected | deferred
    Item: PENDING-NNN
    Source: channels
    Session: superskill (tmux)
    Files changed: [list]

The Iron Principle applies to mobile approvals exactly as it does on
desktop. The model proposes. You decide. The Super Skill records.

---

## Known Limitations

- **Telegram and Discord only.** Slack and WhatsApp are not supported
  by Claude Code Channels at this time.

- **Messages sent while the session is offline are lost permanently.**
  If your tmux session is stopped or your machine is off, messages sent
  to the bot are not queued. They are discarded. Always confirm the
  session is running before sending commands.

- **All code and data stays local.** The Telegram bot is a remote control
  for your local Claude Code session. No domain knowledge, layer files,
  or PENDING content is stored on Telegram servers beyond the message
  delivery. Your Super Skill repository never leaves your machine.

- **One bot per session.** Each Claude Code session connects to one
  Telegram bot. If you run multiple Super Skills, each needs its own
  tmux session and bot.

---

## Troubleshooting

### Bot not responding

1. Check that the tmux session is still running:
     tmux list-sessions
   If "superskill" is not listed, the session died. Start a new one
   (Step 1) and reconnect Channels.

2. Check that Claude Code is still running inside the tmux session:
     tmux attach -t superskill
   If you see a shell prompt instead of Claude Code, restart it:
     claude --channels .

3. Send /ss-pending again from Telegram.

### Pairing code rejected

- Make sure you are sending the code to the correct bot (the one you
  created in Step 3, not BotFather).
- The pairing code expires after a few minutes. If it has been too long,
  run /telegram:configure again in Claude Code to get a new code.
- Copy the code exactly. No extra spaces or line breaks.

### Session dropped after closing terminal

This happens when Claude Code was started without tmux. The solution:
1. Open a new terminal.
2. Run: tmux new -s superskill
3. Start Claude Code with --channels inside the tmux session.
4. Reconnect Telegram (/telegram:configure, new pairing code).

To prevent this in the future, always start Claude Code inside tmux.

---

*Super Skill v2.7.1 -- April 2026*
*github.com/Asaf-Dahan/super-skill*
