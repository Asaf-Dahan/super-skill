Generate a learning module on any topic within this domain.

## Usage
/ss-learn [topic]

## What this does
Reads SUMMARY.md and CONTEXT.md for the active domain.
Generates a structured learning module specific to your domain and situation.
Saves a NotebookLM-ready summary to notebooks\[topic]-learning.md

## Prompt
Read SUMMARY.md and CONTEXT.md for the active domain.

Generate a complete learning module on: $ARGUMENTS

The module must include:
- What this topic means in the context of this specific domain
- How it applies to this owner's situation and goals
- Key decisions or facts from DECISIONS.md that are relevant
- Common mistakes to avoid in this specific context
- A NotebookLM-ready summary with clear sections, no bullet walls

Save the NotebookLM summary to: notebooks\$ARGUMENTS-learning.md
Replace spaces in the filename with hyphens.
Then run: python scripts\feed_notebook.py
If the script fails, report the error and stop.
