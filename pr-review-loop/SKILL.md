---
name: pr-review-loop
description: Run an iterative developer/reviewer loop on a pull request until all in-scope P0-P2 findings are fixed or legitimately rejected, keeping the PR to one scope, clustering valid out-of-scope findings into separate follow-up PR candidates, and asking the user which clusters to address. Use when the user asks to spawn reviewers, review the current PR repeatedly, address review findings, counter or reject bad findings, commit fixes, split an overloaded PR, or decide when a PR is done.
---

# PR Review Loop

Use this skill as the developer agent. Spawn one reviewer at a time, address the review, commit fixes, and repeat until the PR has no unresolved P0-P2 findings or reaches the defined impasse condition.

Keep the PR to one thesis. The loop's main failure mode is scope creep: a reviewer surfaces a real bug in neighboring code, the developer fixes it because fixing is easy, and an unrelated change lands in the feature branch. A valid finding that falls outside the PR's scope is neither rejected nor fixed in place. It is routed to a canonical spillover cluster, and the user chooses which clusters to address as separate follow-up PRs.

## State

Maintain these items throughout the loop:

- `scope_contract`: The PR's thesis - what it is and is not for. Establish it in round 1 from the PR title, description, and the shape of the existing diff; restate it to every reviewer. Every finding is judged against it. Example: "Adds reusable Skills to the toolbox - main-ui toolbox UI, ai-worker prompt injection, event-processor pass-through. NOT a security sweep of connectors or a change to deploy infra."
- `round`: Start at 1.
- `rejection_list`: Start empty. Add one line per final rejection, with the finding summary and why it is wrong or purely stylistic.
- `spillover_clusters`: Start empty. This is the developer-owned canonical list of valid out-of-scope work. Each cluster is an independently mergeable follow-up PR candidate and records: stable id, title, max severity, findings, likely files, owned commits if any, coupling/dependencies, proposed branch name, proposed PR title, one-line rationale, and disposition (`candidate`, `selected`, `deferred`, `rejected`, or `blocked`).
- `open_findings`: Current P0-P2 findings that still require a fix, concession, counter, spillover routing, or final rejection.

Respect the existing worktree. Do not revert unrelated user changes. Keep every commit to a single scope: never mix in-scope fixes with spillover work, or two different spillover clusters, in one commit. The Split pass relies on this. Commit only when there are fixes from the current round.

## Loop

On round 1, establish `scope_contract` before spawning anyone.

1. Spawn exactly one reviewer with the Reviewer Instructions below. Request the highest available reasoning effort, and include the scope contract, the current rejection list, and the current `spillover_clusters`. On round 1, say the rejection list and spillover clusters are empty.
2. Process every P0-P2 finding with the Finding Playbook.
3. Commit in-scope fixes from the round, one scope per commit, including only files related to the fix.
4. Update `rejection_list` and `spillover_clusters` with this round's outcomes.
5. Start the next round unless a Termination condition is met.

There is no hard cap on rounds.

## Finding Playbook

For each finding, first decide whether it is in scope per `scope_contract`.

In scope:

1. Fix it when the finding is valid or when fixing is lower-risk than disputing it.
2. Counter it only when there is a concrete technical reason the finding is wrong or purely stylistic.
3. Send the counter to the reviewer and ask them to concede or counter back with a new argument.
4. If the reviewer concedes, mark the finding done.
5. If the reviewer counters back with a new argument, make a final call: fix it or reject it. Do not keep debating the same finding.

Out of scope:

- If the finding is also wrong or purely stylistic, reject it.
- If it is valid and worth doing - a real bug, security, correctness, or maintainability issue - do not fix it on the feature branch and do not drop it. Assign it to an existing `spillover_clusters` id or create a new cluster candidate with a reason it does not fit any existing cluster. Tell the reviewer it is routed to follow-up selection, not rejected; it should not be re-raised as a blocker for this PR. This is the case the loop most often gets wrong: a good fix lands in the wrong PR and bloats it.

Legitimate rejection reasons are limited to:

- The finding is wrong.
- The finding is purely stylistic and does not affect correctness, safety, maintainability, or user-facing behavior.

Out of scope is not a rejection reason. A valid out-of-scope finding goes to `spillover_clusters` and is addressed by explicit disposition. Do not reject findings because they are inconvenient, large, annoying, or time-consuming.

Record every final rejection as one line:

```text
- <finding summary> - rejected because <one-line reason>.
```

## Spillover Clustering

The developer owns the canonical cluster list. Reviewers assist clustering, but do not define the final cluster boundaries.

Use these rules:

- Every valid out-of-scope finding must map to exactly one `spillover_clusters` entry.
- No catch-all follow-up PR is allowed. Split unrelated findings into separate clusters, even when they were found in the same review round.
- Merge clusters only when the fixes are technically coupled and cannot safely ship apart.
- Split clusters when their findings are independently mergeable, independently testable, or would produce clearer review as separate PRs.
- Keep cluster ids stable across rounds. Rename titles freely when that makes the cluster clearer.
- Normalize clusters after every reviewer round: merge duplicate names, split overloaded clusters, deduplicate repeated findings, and record dependencies between clusters.
- Treat a valid out-of-scope finding as addressed only when it has one explicit disposition: `selected`, `deferred`, `rejected`, or `blocked`.

When sending work to a reviewer, include the current cluster list and ask the reviewer to either assign each valid out-of-scope finding to an existing cluster id or propose a new cluster with a short reason it does not fit the existing clusters.

## Reviewer Exchange

When countering or deferring a reviewer finding, send the smallest sufficient context:

- The exact finding being disputed or deferred.
- The concrete technical counterargument, or the scope reason it is being routed to a spillover cluster.
- Relevant file paths, code references, test output, or PR scope evidence.
- The current rejection list, if the finding overlaps with prior rejected findings.
- The current `spillover_clusters`, if the finding is out of scope or overlaps existing spillover work.

Ask the reviewer to concede or provide a new argument. If they merely restate the original point, treat that as no new argument.

## Termination

Stop the review rounds when either condition is true:

- No in-scope P0-P2 findings remain.
- A reviewer only re-raises rejected findings without new arguments.

If stopping because of impasse, surface it to the user with the rejection list and the reviewer response that added no new argument.

Before the final summary, run Cluster Selection and then the Split pass for selected clusters only.

## Cluster Selection

After the review rounds stop, present the user with the canonical `spillover_clusters`, not individual findings. For each cluster include:

- Cluster id and title.
- Max severity and finding count.
- Why it is out of scope for the feature PR.
- Why the included findings belong together.
- Likely files or commits.
- Dependencies on other clusters.
- Recommended action: select, defer, reject, or block for a user/business decision.

Ask the user which clusters to address now. Do not implement, push, or open PRs for unselected clusters. Mark unselected valid clusters as `deferred` unless the user explicitly rejects or blocks them.

## Split pass

Partition the accumulated work by scope so the feature PR carries only its thesis. This also cleans up scope that leaked into the feature branch in earlier rounds.

1. List every commit and changed file made during the loop. Bucket each as feature-branch (in scope per `scope_contract`) or exactly one selected `spillover_clusters` entry.
2. Check the selected clusters respect coupling: changes that force each other must ship together (a new migration + the deploy-gating and secrets it forces; a webhook auth change + its SSM/config change). Sanity-test each selected cluster: would it build, test, and make sense merged on its own?
3. For each selected spillover cluster, prepare one follow-up PR branch off the base (usually main) carrying only that cluster's commits (cherry-pick), a title and description, and removal of those commits from the feature branch so the feature PR is left with only in-scope changes.
4. Re-run the repo's affected tests/build on the feature branch and each selected follow-up branch.
5. Default to preparing the branches and a split plan, then stop for the user before pushing or opening PRs. Push or open PRs only when the user has authorized it.

The split plan lists, per selected cluster: the files/commits, proposed branch name, title, dependencies, and one-line rationale. Also list deferred, rejected, and blocked clusters separately so valid out-of-scope findings are not lost.

## Final summary

When stopping, summarize:

- Number of review rounds.
- Commits made.
- The split: the feature PR and each selected follow-up PR (or the split plan, if not yet opened).
- Deferred, rejected, and blocked spillover clusters.
- Remaining rejection list, if any.
- Verification performed.

## Reviewer Instructions

Pass this block verbatim when spawning each reviewer:

```text
Review the current PR with extra-high reasoning effort.
- The PR's scope contract is attached. Judge every finding against it.
- The current spillover cluster list is attached. For valid out-of-scope findings, assign the finding to an existing cluster id or propose a new cluster with a short reason it does not fit the existing clusters.
- Severity P0-P3. Report only P0-P2; P3 is noise.
- Flag any repeated code or missed modularization opportunities.
- Tag each finding in-scope or out-of-scope for this PR. For out-of-scope findings, say whether they are still valid and worth fixing (a follow-up PR) or rejectable, propose cluster placement, and note any coupling to other findings (changes that must ship together). Out-of-scope is not a reason to skip reporting; report it tagged so it can be routed, not dropped or jammed into this PR.
- A rejection list from prior rounds may be attached. For each item, concede or counter with a new argument. Do not re-raise.
- When the developer counters or defers your finding: concede or counter back with a new argument. Do not restate the original point.
```
