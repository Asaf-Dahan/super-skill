Check all monitoring sources for changes in the active domain.

## Usage
/ss-drift

## What this does
Reads MONITORING.md for the active domain.
Checks each source URL for availability and recent changes.
Writes any detected drift to PENDING.md as DRIFT-NNN.
Does not update CURRENT_STATE.md directly.

## Prompt
Read MONITORING.md for the active domain.

For each source listed:
- Check if the URL is reachable
- Note the check date and time
- Flag any source that returns an error or unexpected response

Write a DRIFT-NNN item to PENDING.md for any source that shows a problem.
End with a summary: "Checked N sources. N alerts written to PENDING.md."
Do not modify CURRENT_STATE.md or any other layer file.
