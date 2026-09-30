# Personal Agent Skills

Reusable agent skills, loaded by both Codex and Claude Code.

## Skills

- `pr-review-loop` - Iterative developer/reviewer loop until P0-P2 findings are fixed or legitimately rejected; keeps the PR to one scope and clusters valid out-of-scope findings into user-selected follow-up PRs.
- `merge-origin-main` - Merge `origin/main` into the current branch, resolve conflicts as integration work, verify, and push.
- `split-overgrown-pr` - Analyze an overloaded PR, explain why changes exist, and plan cluster-level PR splits.
- `revive-stale-pr` - Pick up an old PR: decide if it is still needed, bring it current, and plan the production rollout with manual steps flagged.
- `fork-herdr` - Fork the current Claude Code session into a new herdr tab and its own git worktree to chase a side issue while the original session continues.

## Local Installation

From this checkout, run:

```bash
python3 scripts/install_skills.py
```

The installer discovers every top-level `SKILL.md` and links its directory into:

- `~/.agents/skills` for Codex, following the [official skill discovery documentation](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills).
- `~/.claude/skills` for Claude Code.

Both tools read the same source files. Rerunning the installer is safe: it leaves correct links in place and refuses to overwrite local copies or links to another checkout. It removes legacy `~/.codex/skills` links only when they point to the same skill in this checkout.

For project-scoped installs, use `<project>/.agents/skills` for Codex or `<project>/.claude/skills` for Claude Code.

### If a skill is missing

Rerun the installer and restart Codex if the skill list has not refreshed. Check `~/.codex/config.toml` (or `$CODEX_HOME/config.toml` when set) for a `[[skills.config]]` entry targeting the skill's `SKILL.md`. An entry with `enabled = false` disables an otherwise valid installation; change it to `true` to re-enable that skill and restart Codex.

## Authoring and Updating

Conventions for writing skills live in `AGENTS.md`. Edit skills here, validate, then commit and push. Never edit the installed symlink paths directly.
