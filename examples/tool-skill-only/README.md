# Example: SKILL.md without a Super Skill

Some domains do not need a Super Skill.
This example shows when a single SKILL.md file is the right choice
and how to structure it.

---

## The Domain: Lovable Prompt Engineering

This skill tells Claude how to write atomic prompts for Lovable.
It does not need a Super Skill because:

- No external drift: the methodology is controlled by the owner
- No decisions to protect: the philosophy is in the SKILL.md itself
- No current state needed: no tool version or plan to track

The three-question test returns zero YES answers for this domain.

---

## The Three-Question Test

Before creating a Super Skill, ask:

1. Does this domain change externally without your control?
2. Are there decisions that must never be re-litigated?
3. Does your agent need verified current state before every task?

If fewer than two answers are YES: a SKILL.md file is sufficient.

---

## Rule of Thumb

If you write the same guidance every session: put it in SKILL.md.

If the tool you are writing about released an update this week and
you are not sure whether your guidance still applies: you need a
Super Skill with MONITORING.md watching that tool's changelog.

---

## File Structure

```
my-skills/
  .claude/
    skills/
      my-prompt-engineer/
        SKILL.md
```

No CONTEXT.md. No DECISIONS.md. No PENDING.md.
Just the skill file and nothing more.

---

## When to Upgrade to a Super Skill

Start with SKILL.md. Upgrade when you notice:

- You are correcting the agent because it used outdated information
- You keep re-explaining the same architectural decisions
- A tool you rely on released a major update and your skill is now wrong
- You want multiple agents to share the same domain knowledge
