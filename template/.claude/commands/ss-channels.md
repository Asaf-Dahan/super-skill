Show Channels connection status and available mobile commands.

## Usage
/ss-channels

## What this does
Reports whether Claude Code was started with --channels and whether
a Telegram or Discord bot is currently connected. Lists available
mobile commands if connected.

## Prompt
Check the current Channels connection status.

Detect whether this Claude Code session was started with the --channels flag.
If you cannot detect the flag directly, ask:
  "Was this session started with 'claude --channels .'?
   If not, restart with the --channels flag to enable mobile access."

If the session was started with --channels:
  Check if a Telegram or Discord bot is connected.

  If connected, report:
    "Channels: connected via [Telegram | Discord]

    Available commands from mobile:
      /ss-pending   -- list open PENDING items
      /ss-drift     -- check monitored sources for changes
      /ss-sync      -- pull all Super Skills and check drift
      /ss-council   -- show active expert debates
      /ss-summary   -- return current SUMMARY.md
      /ss-channels  -- show this status

    To approve a PENDING item from mobile, send:
      Approve PENDING-NNN
    All approvals are recorded in LOG.md with source: channels."

  If not connected, report:
    "Channels is enabled but no bot is connected.

    To connect Telegram:
      1. Create a bot via @BotFather on Telegram (/newbot)
      2. Run /telegram:configure in this session
      3. Paste the bot token and send the pairing code

    Full guide: CHANNELS_GUIDE.md"

If the session was NOT started with --channels:
  Report:
    "Channels is not active in this session.
     To enable: restart Claude Code with 'claude --channels .'
     Full setup guide: CHANNELS_GUIDE.md"
