# Personal Agent Skills

Private repository for reusable agent skills, loaded by both Codex and Claude Code.

## Skills

- `pr-review-loop` - Run an iterative developer/reviewer loop until P0-P2 PR findings are fixed or legitimately rejected.
- `pr-review-loop-v2` - Same loop, but keeps the PR to one scope and clusters valid out-of-scope findings into user-selected follow-up PRs.
- `merge-origin-main` - Merge `origin/main` into the current branch, resolve conflicts as integration work, verify, and push.
- `split-overgrown-pr` - Analyze an overloaded PR, explain why changes exist, and plan cluster-level PR splits.
- `revive-stale-pr` - Pick up an old PR: decide if it is still needed, bring it current, and plan the production rollout with manual steps flagged.

## Local Installation

Install by symlink so both tools load the same files and edits in this repo take effect immediately:

```bash
for s in pr-review-loop pr-review-loop-v2 merge-origin-main split-overgrown-pr revive-stale-pr; do
  ln -sfn /Users/pol/repos/pol-skills/$s /Users/pol/.codex/skills/$s
  ln -sfn /Users/pol/repos/pol-skills/$s /Users/pol/.claude/skills/$s
done
```

For a project-scoped Claude Code install, create the same symlinks under `<project>/.claude/skills`.

## Authoring and Updating

Conventions for writing skills live in `AGENTS.md`. Edit skills here, validate, then commit and push. Never edit the installed symlink paths directly.
