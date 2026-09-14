---
name: merge-origin-main
description: Fetch origin/main, merge it into the current branch, resolve conflicts as integration work, review the merged result for consistency with the branch, verify, and push. Use when the user asks to update the current branch from main, merge main, bring a branch up to date, solve merge conflicts, or push the merged branch.
---

# Merge Origin Main

Integrate the latest `origin/main` into the checked-out branch so the branch reads as if it had been written on top of current main, then push.

## Guardrails

- Merge; do not rebase unless the user asks.
- Do not stash, commit, discard, or revert the user's uncommitted changes without asking. If they would block a safe merge, stop and ask.
- Never resolve a conflict by taking one side wholesale. Read both sides and the surrounding code, and keep the intent of each unless one clearly supersedes the other.
- Push only when the merge is committed, verification has run, and the tree is clean apart from the user's own changes.

## What a good result looks like

- No conflict markers anywhere in the tree.
- The branch's changes still work against what main changed underneath them: renamed or removed symbols, changed signatures, moved files, new conventions, regenerated artifacts, and tests whose expectations moved. Review the whole merge diff for this, not only files that conflicted textually.
- The repo's relevant verification passed: affected tests, type checks, linters, generators, build. Prefer the repo's own affected-tests helper if it has one. If something cannot run, say so instead of skipping silently.
- Post-merge fixes, if any, are committed separately from the merge commit so they stay reviewable.

## Report

Branch merged and pushed; conflicts resolved and where; integration fixes beyond conflict resolution; verification run and results; anything left unverified.
