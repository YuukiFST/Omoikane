### Authoring or modifying a skill

**You own the skill's voice.**

1. Use the **writing-for-agents** skill.
2. Validate the skill: frontmatter has `name` and `description`, the description is under 1,024 characters (Pi's cap), referenced files exist, cross-skill links resolve, no file below the skill folder is named `SKILL.md`, and no Markdown file sits directly in `.claude/skills/`. Pi 1.0.4 loads each Markdown file placed directly in a skills folder as a skill, and stops descending at a folder that holds `SKILL.md`, so a nested `SKILL.md` never loads there.
3. Test cases if structural. Skip if subjective.
4. Run **Opening a PR**.

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per principle `encode-lessons-in-structure`. Delegate to other skills by path. Don't restate. A workflow you keep hitting but isn't captured → propose a new skill.

**Reply:** summary of the skill, key design decisions, validation notes.

Adapted from pstack `skills/poteto-mode/playbooks/authoring-a-skill.md` at df58112. MIT, see `../LICENSE`.
