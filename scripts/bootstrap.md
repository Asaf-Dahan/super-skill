You are setting up a Super Skill.
Work through the following steps in order.
Stop and explain clearly if anything is missing before continuing.

STEP 1: Environment Check

Check git:
  run: git --version

If git is NOT installed, stop and tell the user:
  "Git is not installed.
   Git downloads the Super Skill template to your computer.
   Download it here: https://git-scm.com/download
   Windows: run the installer, keep all default settings.
   Mac: run the installer or type 'xcode-select --install' in Terminal.
   After installing, come back and paste this prompt again."

Check Python:
  run: python3 --version
  if that fails try: python --version

If Python is NOT installed, stop and tell the user:
  "Python is not installed.
   Python runs the Super Skill scripts.
   Download it here: https://python.org/downloads
   Windows: run the installer. Check the box that says
   'Add Python to PATH' before clicking Install.
   Mac: run the installer.
   After installing, come back and paste this prompt again."

Report: git version, python version, working directory. Then continue.

STEP 2: Domain Name and Description

Ask the user exactly this and wait for the answer:
  "What is your domain?
   This becomes the name of your Super Skill folder.
   Examples: garden, investments, fitness, marketing, stack
   One word or short phrase, no spaces."

Use the answer as [domain] in all following steps.

Then ask:
  "Describe your domain in one to three sentences.
   What does it cover? What are you building or managing?"

Use the answer as [domain-description] in Step 5.

Then ask:
  "What do you want to achieve with this Super Skill? One sentence."

Use the answer as [domain-goal] in Step 5.

STEP 3: Clone

run: git clone https://github.com/Asaf-Dahan/super-skill.git super-skill-[domain]

Forking this template? Replace the URL above with your own fork's URL.

Confirm all template files are present before continuing.

If you plan to use NotebookLM: copy .env.example to .env
and add your notebook ID after completing the NotebookLM setup
in NOTEBOOKLM_GUIDE.md.

STEP 4: Git Identity

Check:
  git -C super-skill-[domain] config user.name
  git -C super-skill-[domain] config user.email

If either is empty, ask:
  "What name should appear on your saved changes?"
  "What email address should be linked to them?"

Then set them:
  git -C super-skill-[domain] config user.name "[name]"
  git -C super-skill-[domain] config user.email "[email]"

STEP 5: Activate

Change into the cloned repository first:
  cd super-skill-[domain]

Read: SUPER_SKILL_MANIFESTO.md
Read: ONBOARDING.md

Run Prompt 1 from ONBOARDING.md in full.
All file operations happen inside this folder.
All generated files go here. Do not ask the user to copy Prompt 1.
Run it yourself.

When Prompt 1 reaches the placeholders at the end, fill them in
using the answers collected in Step 2:
  My domain: [domain-description]
  What I want to achieve: [domain-goal]
Do not ask the user again. Use the answers already collected.

STEP 6: First Commit

After all files are generated and SUMMARY.md exists:

git -C super-skill-[domain] add .
git -C super-skill-[domain] commit -m "feat: activate Super Skill -- [domain]"

STEP 7: Back up to GitHub (optional)

Ask the user exactly this and wait for the answer:
  "Do you want to save your Super Skill to GitHub?
   This keeps a backup online and lets you access it
   from any computer. You will need a free GitHub account
   at https://github.com
   Answer yes or no."

If yes:
  Check if GitHub CLI is available:
    gh --version

  If gh IS available:
    Run:
      gh repo create super-skill-[domain] --private --source=super-skill-[domain] --remote=origin --push
    Capture the returned URL.
    Add a line to CONTEXT.md under the identity or header section:
      Repository: [URL]
    Tell the user:
      "Repository created and pushed automatically.
       The remote URL has been recorded in CONTEXT.md."

  If gh is NOT available:
    Tell the user:
      "GitHub CLI is not installed.
       Go to https://github.com/new
         - Repository name: super-skill-[domain]
         - Visibility: Private
         - Leave all checkboxes unchecked
         - Click 'Create repository'

       After the page reloads, look for the section titled:
         '...or push an existing repository from the command line'
       Copy the URL from that section. It looks like:
         https://github.com/your-username/super-skill-[domain].git

       Paste it here."

    Wait for the URL. Then run:
      git -C super-skill-[domain] remote set-url origin [URL]
      git -C super-skill-[domain] push -u origin main

    Add a line to CONTEXT.md under the identity or header section:
      Repository: [URL]
    Tell the user:
      "Your Super Skill is backed up to GitHub.
       The remote URL has been recorded in CONTEXT.md."

If no:
  Add this item to PENDING.md under the Queue section:

    ### PENDING-001: GitHub backup not configured
    Type: update
    Proposed: [today's date]
    Summary: GitHub backup was skipped during activation. To add later: create a repository at https://github.com/new, then run git remote set-url origin [URL] followed by git push -u origin main.
    Affected layers: CONTEXT.md
    Recommended action: adopt when ready
    Decision:
    Outcome:

  Tell the user:
    "Skipped. Your Super Skill is saved locally only.
     A reminder has been added to PENDING.md.
     Run /ss-pending when you are ready to set up GitHub backup."

Then tell the user:
  "Your Super Skill is live.
   To open it next time: open Claude Code on the
   super-skill-[domain] folder.
   Use /ss-eval, /ss-learn, /ss-pending and other
   slash commands for everything from here.

   Optional next step: connect the NotebookLM learning layer.
   See NOTEBOOKLM_GUIDE.md to generate audio, quizzes, and mind maps
   from your domain knowledge."
