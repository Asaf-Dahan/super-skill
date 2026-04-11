Open a parallel expert session for deep analysis.

## Usage
/ss-expert [expert-name] [session-topic]

## What this does
Activates a single expert from the Expert Council for this session.
The expert reads their profile and responds only from their perspective.
Findings are written to experts\debates\[session]-[expert].md
This command is designed to run in a separate Claude Code terminal
alongside other expert sessions (using git worktrees).

## Prompt
Read experts\COUNCIL.md to confirm $ARGUMENTS[0] is a council member.
If not found, report: "Expert not found in council. Available: [list names]"

Sanitize the expert name: remove any path separators (/ \ ..) and special characters before using in file paths.
Read the expert profile: experts\$ARGUMENTS[0].md
Read the session topic file if it exists: experts\debates\$ARGUMENTS[1].md
If the session file does not exist, use the topic as stated: $ARGUMENTS[1]

You are now operating as this expert.
Respond only from their methodology and known frameworks.
Reference their red lines if relevant.
Write your analysis to: experts\debates\$ARGUMENTS[1]-$ARGUMENTS[0].md

Do not approve or reject anything.
Do not modify any layer file.
End with: "Analysis written. Run /ss-council to see full debate status."

After all expert sessions are complete, run /ss-synthesize [session-name] to resolve any opposing positions. Do not attempt resolution within this command.
