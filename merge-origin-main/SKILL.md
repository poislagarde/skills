---
name: merge-origin-main
description: Fetch origin/main, merge it into the current branch, resolve conflicts, review the integrated code for consistency with the branch, verify the result, and push. Use when the user asks to update the current branch from origin/main, merge main, solve merge conflicts, or push the merged branch.
---

# Merge Origin Main

Use this skill to integrate the latest `origin/main` into the currently checked-out branch, resolve conflicts thoughtfully, review the merged code, and push the branch.

## Ground Rules

- Merge `origin/main`; do not rebase unless the user explicitly changes the request.
- Do not overwrite or revert unrelated user changes.
- Do not resolve conflicts by blindly accepting `ours`, `theirs`, or conflict markers.
- Treat conflict resolution as integration work: preserve the intent of both `origin/main` and the current branch where possible.
- Push only after the merge is committed, the working tree is clean except for intentional uncommitted user changes, and relevant verification has run.

## Workflow

1. Inspect the repository state:
   - Run `git status --short` and `git branch --show-current`.
   - Identify existing uncommitted changes before fetching or merging.
   - If unrelated dirty changes would block a safe merge, stop and ask how to handle them. Do not stash, commit, or discard unrelated work without explicit user approval.
2. Fetch the target branch:
   - Run `git fetch origin main`.
   - Confirm `origin/main` updated successfully.
3. Merge into the current branch:
   - Run `git merge origin/main`.
   - If the merge succeeds without conflicts, continue to the review step.
   - If conflicts occur, resolve all unmerged files before committing.
4. Resolve conflicts:
   - Use `git status --short` and `git diff --name-only --diff-filter=U` to identify unmerged paths.
   - Read the conflicted files and nearby related code before editing.
   - Preserve current-branch behavior unless `origin/main` intentionally supersedes it.
   - Preserve new mainline behavior unless the current branch intentionally changes that area.
   - After each resolution, search for conflict markers with `rg '<<<<<<<|=======|>>>>>>>'`.
   - Stage only resolved, intentional files.
5. Review all new and changed code:
   - Review the merge diff, not just files with textual conflicts.
   - Compare changed files against both sides when needed using `git diff HEAD`, `git diff origin/main...HEAD`, and relevant file history.
   - Look for duplicated logic, missed abstractions, stale imports, incompatible APIs, renamed symbols, generated files that need regeneration, and tests that no longer match behavior.
   - Adjust code so the result is consistent with the current branch's design and with the incoming `origin/main` changes.
6. Verify:
   - Run the most relevant available tests, linters, type checks, generators, or build commands for the affected code.
   - If the repo has an affected-test helper, prefer it.
   - If verification cannot run, record the reason.
7. Complete the merge:
   - If conflicts were resolved, run `git status` and then `git commit` to complete the merge commit.
   - If the merge already committed automatically, do not create an extra commit unless fixes were needed after the merge.
   - If post-merge fixes were needed after an automatic merge commit, commit those fixes separately with a focused message.
8. Push:
   - Confirm the current branch name.
   - Push the current branch to its upstream with `git push`.
   - If no upstream is configured, use `git push -u origin <current-branch>`.

## Final Response

Report:

- The branch merged and pushed.
- Whether conflicts occurred and which files were resolved.
- Any extra integration fixes made during review.
- Verification commands run and their results.
- Any remaining risks or verification that could not be completed.
