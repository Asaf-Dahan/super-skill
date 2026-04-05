# Example: SKILL.md without a Super Skill

Some domains do not need a Super Skill. This example shows when a
single SKILL.md file is the right choice and how to structure it.

## The domain: Lovable prompt engineering

This skill tells Claude HOW to write atomic prompts for Lovable.
It does not need a Super Skill because:

- No external drift: the methodology is controlled by the owner
- No decisions to protect: the philosophy is in the SKILL.md itself
- No current state needed: no tool version or plan to track

The three-question test gives zero YES answers for this domain.

## Rule of thumb

If you write the same guidance every session: put it in SKILL.md.

If the tool you are writing about released an update this week and
you are not sure whether your guidance still applies: you need a
Super Skill with MONITORING.md watching that tool's changelog.

## File structure

```
az-skills/
└── .claude/
    └── skills/
        └── lovable-prompt-engineer/
            └── SKILL.md
```

No CONTEXT.md. No DECISIONS.md. No PENDING.md.
Just the skill file - and nothing more.
