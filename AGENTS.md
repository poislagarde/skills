# Agent Notes

This repository is the canonical source for Pol's personal agent skills. They load in both Codex and Claude Code.

## Layout

Each top-level directory that contains `SKILL.md` is a skill. Each skill has `SKILL.md` and, for Codex, `agents/openai.yaml`. Do not add auxiliary docs (README, CHANGELOG, notes) inside skill directories. Repo-level docs live in `README.md` and this file.

## Skill Authoring Conventions

These follow Anthropic's skill best practices (https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/best-practices). The ones that matter most for this repo:

- **Assume the model is smart; match specificity to fragility.** Write only what it does not already know: this repo's process, guardrails, and judgment calls. Exact steps and commands only where a wrong move is costly or irreversible: rewriting history, pushing, deploying, deleting. Everywhere else describe the outcome and the guardrails and let the model pick the route. "Run the repo's relevant verification" beats a list of commands. This is deliberate: it leaves room for models to add value as they improve, and a loaded skill stays in context all session, so every line must justify its token cost.
- **The description does the triggering.** It is the only part loaded before a skill is chosen. Write it in third person, say what the skill does and when to use it, and include the phrases a user would actually type. Keep "when to use" out of the body. Descriptions of different skills must be distinguishable from each other.
- **Agent-neutral wording.** Say "the agent" or nothing. Never name Codex or Claude in `SKILL.md`; `agents/openai.yaml` is the one Codex-specific file.
- **One default, with an escape hatch.** Do not list alternative approaches. Give a sensible default output format and say it may be adapted.
- **Reuse skills by name** (for example, "use the `merge-origin-main` skill") instead of restating their steps.
- **Name**: lowercase letters, numbers, and hyphens, at most 64 characters, matching the directory name, and not containing `claude` or `anthropic`.
- **Length**: aim well under Anthropic's 500-line limit. Move long reference material to a `references/` file one level deep and link it from `SKILL.md`.
- **No time-sensitive content**: no dates, version-gated instructions, or "old patterns" sections.
- **Consistent terminology** within a skill (pick "finding" or "issue", not both).
- **Try it before you ship it.** Run a rewritten skill once on a real task before committing.

## Installation

Every skill directory here is symlinked under the same name into `/Users/pol/.codex/skills` and `/Users/pol/.claude/skills`, so both tools load the same files and edits take effect immediately. The command is in `README.md`. For a project-scoped Claude Code install, use `<project>/.claude/skills` instead.

If an installed path is a real directory instead of a symlink, replace it with a symlink after confirming the repo copy is current.

## Workflow

- Treat this repo as the source of truth. Edit here, never at the installed path.
- After changing a skill, run the validator:

  ```bash
  python3 /Users/pol/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/pol/repos/pol-skills/<skill-name>
  ```

- Commit and push to `origin`.
- When adding or removing a skill, also update the symlinks in both tools and the skill list in `README.md`.
