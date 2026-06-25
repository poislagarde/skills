---
name: pr-review-loop
description: Run an iterative developer/reviewer loop on a pull request until all P0-P2 findings are fixed or legitimately rejected. Use when the user asks Codex to spawn reviewers, review the current PR repeatedly, address review findings, counter or reject bad findings, commit fixes, or decide when a PR is done.
---

# PR Review Loop

Use this skill as the developer agent. Spawn one reviewer at a time, address the review, commit fixes, and repeat until the PR has no unresolved P0-P2 findings or reaches the defined impasse condition.

## State

Maintain these items throughout the loop:

- `round`: Start at 1.
- `rejection_list`: Start empty. Add one line for each final rejection, including the finding summary and the reason it is wrong, out of scope, or stylistic.
- `open_findings`: Current P0-P2 findings that still require a fix, concession, counter, or final rejection.

Respect the existing worktree. Do not revert unrelated user changes, and do not include unrelated changes in commits. Commit only when there are fixes from the current round.

## Loop

1. Spawn exactly one reviewer with the Reviewer Instructions below. Request the highest available reasoning effort, and include the current rejection list. On round 1, say the rejection list is empty.
2. Process every P0-P2 finding with the Finding Playbook.
3. Commit fixes from the round. Use focused commit messages and include only files related to the fixes.
4. Update `rejection_list` with any final rejections from this round.
5. Start the next round unless a Termination condition is met.

There is no hard cap on rounds.

## Finding Playbook

For each finding:

1. Fix it when the finding is valid or when fixing is lower-risk than disputing it.
2. Counter it only when there is a concrete technical reason the finding is wrong, out of scope, or stylistic.
3. Send the counter to the reviewer and ask them to either concede or counter back with a new argument.
4. If the reviewer concedes, mark the finding done.
5. If the reviewer counters back with a new argument, make a final call: fix it or reject it. Do not continue debating the same finding.

Legitimate rejection reasons are limited to:

- The finding is wrong.
- The finding is out of scope for the PR.
- The finding is stylistic and does not affect correctness, safety, maintainability, or user-facing behavior.

Do not reject findings because they are inconvenient, large, annoying, or time-consuming.

Record every final rejection as one line:

```text
- <finding summary> - rejected because <one-line reason>.
```

## Reviewer Exchange

When countering a reviewer finding, send the smallest sufficient context:

- The exact finding being disputed.
- The concrete technical counterargument.
- Relevant file paths, code references, test output, or PR scope evidence.
- The current rejection list, if the finding overlaps with prior rejected findings.

Ask the reviewer to concede or provide a new argument. If they merely restate the original point, treat that as no new argument.

## Termination

Stop when either condition is true:

- No P0-P2 findings remain.
- A reviewer only re-raises rejected findings without new arguments.

If stopping because of impasse, surface it to the user with the rejection list and the reviewer response that added no new argument.

When stopping normally, summarize:

- Number of review rounds.
- Commits made.
- Remaining rejection list, if any.
- Verification performed.

## Reviewer Instructions

Pass this block verbatim when spawning each reviewer:

```text
Review the current PR with extra-high reasoning effort.
- Severity P0-P3. Report only P0-P2; P3 is noise.
- Flag any repeated code or missed modularization opportunities.
- A rejection list from prior rounds may be attached. For each item, concede or counter with a new argument. Do not re-raise.
- When the developer counters your finding: concede or counter back with a new argument. Do not restate the original point.
```
