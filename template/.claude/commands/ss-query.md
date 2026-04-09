Search wiki notes by keyword and return matching entries.

## Usage
/ss-query [keyword or phrase]

## What this does
Searches all .md files in the wiki/ directory for the given keyword.
Returns matching file names and the lines containing the match.
If no matches found, reports: "No wiki entries match '[keyword]'."
Does not modify any files.

## Prompt
Search all .md files inside the wiki/ directory for: $ARGUMENTS

For each file that contains a match:
- Show the filename
- Show each line containing the keyword with 1 line of context above and below
- If the file has a # heading on line 1, show that as the entry title

If no files exist in wiki/ (besides README.md and .gitkeep), report:
"wiki/ is empty. Add .md files to build your knowledge base."

If no matches are found, report:
"No wiki entries match '$ARGUMENTS'."

Do not modify any files. Read-only operation.
