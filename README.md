# Personal Codex Skills

Private repository for reusable Codex skills.

## Skills

- `pr-review-loop` - Run an iterative developer/reviewer loop until P0-P2 PR findings are fixed or legitimately rejected.
- `pr-review-loop-v2` - Keep a PR scoped while clustering valid out-of-scope findings into user-selected follow-up PRs.
- `merge-origin-main` - Fetch `origin/main`, merge it into the current branch, resolve conflicts, review the result, verify, and push.
- `split-overgrown-pr` - Analyze an overloaded PR, explain why changes exist, and plan cluster-level PR splits.

## Local Installation

These skills are intended to be installed by symlink from Codex's local skills directory:

```bash
ln -s /Users/pol/repos/pol-skills/pr-review-loop /Users/pol/.codex/skills/pr-review-loop
ln -s /Users/pol/repos/pol-skills/pr-review-loop-v2 /Users/pol/.codex/skills/pr-review-loop-v2
ln -s /Users/pol/repos/pol-skills/merge-origin-main /Users/pol/.codex/skills/merge-origin-main
ln -s /Users/pol/repos/pol-skills/split-overgrown-pr /Users/pol/.codex/skills/split-overgrown-pr
```

When installed this way, editing the repo copy updates the active Codex skill immediately.

## Updating Skills

Edit skills in this repository, then commit and push:

```bash
git status
git add <skill>
git commit -m "Update <skill>"
git push
```

Avoid editing copied skill folders under `/Users/pol/.codex/skills`. Those paths should be symlinks back to this repository.
