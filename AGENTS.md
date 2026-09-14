# Agent Notes

This repository is the canonical source for Pol's personal agent skills. They load in both Codex and Claude Code.

## Layout

Each top-level directory that contains `SKILL.md` is a skill:

- `pr-review-loop-v2/`
- `merge-origin-main/`
- `split-overgrown-pr/`
- `revive-stale-pr/`

Each skill has `SKILL.md` and, for Codex, `agents/openai.yaml`. Do not add auxiliary docs (README, CHANGELOG, notes) inside skill directories. Repo-level docs live in `README.md` and this file.

## Skill Authoring Conventions

These follow Anthropic's skill best practices (https://platform.claude.com/docs/en/docs/agents-and-tools/agent-skills/best-practices). The ones that matter most for this repo:

- **Assume the model is smart.** Write only what it does not already know: this repo's process, guardrails, and judgment calls. Do not explain git, GitHub, or general engineering. A loaded skill stays in context for the whole session, so every line must justify its token cost.
- **Match specificity to fragility.** Exact steps and commands only where a wrong move is costly or irreversible: rewriting history, pushing, deploying, deleting. Everywhere else describe the outcome and the guardrails and let the model pick the route. "Run the repo's relevant verification" beats a list of commands. This is deliberate: it leaves room for models to add value as they improve.
- **The description does the triggering.** It is the only part loaded before a skill is chosen. Write it in third person, say what the skill does and when to use it, and include the phrases a user would actually type. Keep "when to use" out of the body. Descriptions of different skills must be distinguishable from each other.
- **Agent-neutral wording.** Say "the agent" or nothing. Never name Codex or Claude in `SKILL.md`; `agents/openai.yaml` is the one Codex-specific file.
- **One default, with an escape hatch.** Do not list alternative approaches. Give a sensible default output format and say it may be adapted.
- **Reuse skills by name** (for example, "use the `merge-origin-main` skill") instead of restating their steps.
- **Name**: lowercase letters, numbers, and hyphens, at most 64 characters, matching the directory name, and not containing `claude` or `anthropic`.
- **Length**: current skills are 30 to 155 lines and that is the right range. Anthropic's hard limit is 500. Move long reference material to a `references/` file one level deep and link it from `SKILL.md`.
- **No time-sensitive content**: no dates, version-gated instructions, or "old patterns" sections.
- **Consistent terminology** within a skill (pick "finding" or "issue", not both).

## Installation Model

Use symlinks so Codex and Claude Code both load the same files from this repository.

### Codex

The installed Codex skill paths should be symlinks back to this repo:

```bash
/Users/pol/.codex/skills/pr-review-loop-v2 -> /Users/pol/repos/pol-skills/pr-review-loop-v2
/Users/pol/.codex/skills/merge-origin-main -> /Users/pol/repos/pol-skills/merge-origin-main
/Users/pol/.codex/skills/split-overgrown-pr -> /Users/pol/repos/pol-skills/split-overgrown-pr
/Users/pol/.codex/skills/revive-stale-pr -> /Users/pol/repos/pol-skills/revive-stale-pr
```

If a path under `/Users/pol/.codex/skills` is a real directory instead of a symlink, replace it with a symlink after confirming the repo copy is current.

### Claude Code

The installed global Claude Code skill paths should also be symlinks back to this repo:

```bash
/Users/pol/.claude/skills/pr-review-loop-v2 -> /Users/pol/repos/pol-skills/pr-review-loop-v2
/Users/pol/.claude/skills/merge-origin-main -> /Users/pol/repos/pol-skills/merge-origin-main
/Users/pol/.claude/skills/split-overgrown-pr -> /Users/pol/repos/pol-skills/split-overgrown-pr
/Users/pol/.claude/skills/revive-stale-pr -> /Users/pol/repos/pol-skills/revive-stale-pr
```

Use `/Users/pol/.claude/skills` for global Claude Code availability. For project-scoped Claude Code installation, create the same symlinks under `<project>/.claude/skills` instead.

If a path under `/Users/pol/.claude/skills` or `<project>/.claude/skills` is a real directory instead of a symlink, replace it with a symlink after confirming the repo copy is current.

## Keeping Skills In Sync

- Treat `/Users/pol/repos/pol-skills` as the source of truth.
- Edit the repo copy, not the installed symlink path, unless you have confirmed the installed path resolves into this repo.
- After changing a skill, validate `SKILL.md` frontmatter and `agents/openai.yaml` if present.
- Commit skill changes in this repo and push to `origin`.
- When adding a new skill, add the top-level skill directory here, create matching symlinks in `/Users/pol/.codex/skills` and `/Users/pol/.claude/skills`, update `README.md` and this file, and commit everything.

## Validation

Prefer the bundled validator when available:

```bash
python3 /Users/pol/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/pol/repos/pol-skills/<skill-name>
```

If the validator cannot run because `PyYAML` is unavailable, manually check that:

- `SKILL.md` exists.
- Frontmatter has `name` and `description`.
- `name` is lowercase hyphen-case.
- `description` is plain text without angle brackets.
- `agents/openai.yaml`, when present, has quoted `display_name`, `short_description`, and `default_prompt`.
