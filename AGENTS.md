# Agent Notes

This repository is the canonical source for Pol's personal agent skills.

## Layout

Each top-level directory that contains `SKILL.md` is a skill:

- `pr-review-loop/`
- `pr-review-loop-v2/`
- `merge-origin-main/`
- `split-overgrown-pr/`

Do not add auxiliary docs inside skill directories unless they are required skill resources. Keep repo-level docs in `README.md` or `AGENTS.md`.

## Installation Model

Use symlinks so Codex and Claude Code both load the same files from this repository.

### Codex

The installed Codex skill paths should be symlinks back to this repo:

```bash
/Users/pol/.codex/skills/pr-review-loop -> /Users/pol/repos/pol-skills/pr-review-loop
/Users/pol/.codex/skills/pr-review-loop-v2 -> /Users/pol/repos/pol-skills/pr-review-loop-v2
/Users/pol/.codex/skills/merge-origin-main -> /Users/pol/repos/pol-skills/merge-origin-main
/Users/pol/.codex/skills/split-overgrown-pr -> /Users/pol/repos/pol-skills/split-overgrown-pr
```

If a path under `/Users/pol/.codex/skills` is a real directory instead of a symlink, replace it with a symlink after confirming the repo copy is current.

### Claude Code

The installed global Claude Code skill paths should also be symlinks back to this repo:

```bash
/Users/pol/.claude/skills/pr-review-loop -> /Users/pol/repos/pol-skills/pr-review-loop
/Users/pol/.claude/skills/pr-review-loop-v2 -> /Users/pol/repos/pol-skills/pr-review-loop-v2
/Users/pol/.claude/skills/merge-origin-main -> /Users/pol/repos/pol-skills/merge-origin-main
/Users/pol/.claude/skills/split-overgrown-pr -> /Users/pol/repos/pol-skills/split-overgrown-pr
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
