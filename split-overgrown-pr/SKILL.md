---
name: split-overgrown-pr
description: Analyze a pull request that may have grown out of scope, explain why review-agent or follow-up changes were made, classify changes against the PR thesis, cluster out-of-scope work into independently mergeable pieces, and produce a user-approved split plan. Use when returning to an old PR, auditing review-agent changes, deciding what belongs in the current PR, or breaking an overloaded PR into smaller PRs.
---

# Split Overgrown PR

Use this skill when a PR has accumulated extra changes and the user needs to understand what happened, what still belongs in the current PR, and what should become separate PRs.

The default mode is analysis-first. Do not move code, rewrite history, push branches, or open PRs until the user approves a cluster-level split plan.

## Goals

- Recover the PR's intended thesis.
- Explain why each meaningful change appears to exist.
- Separate confirmed evidence from inference.
- Classify work as in scope, out of scope, revert/remove, or needs decision.
- Cluster out-of-scope work into separate follow-up PR candidates.
- Give the user control at the cluster level, not one file or finding at a time.

## Orient

Start by collecting context:

- Current branch, base branch, PR title, PR body, linked issue, and review comments if available.
- Commit history and author/timestamps, especially commits made after review-agent activity started.
- Full diff from base to current branch.
- Test, config, migration, generated, and lockfile changes.
- Existing user instructions in the thread or repo docs.

If GitHub context is available, inspect PR comments and review threads for clues about why changes were made. If it is not available, proceed from local git evidence and label uncertain explanations as inferred.

## Establish Scope

Define a `scope_contract` before classifying changes:

- What the PR is trying to accomplish.
- What files or subsystems are naturally part of that goal.
- What is explicitly not part of that goal.
- Any unavoidable dependencies that must stay with the PR.

Use the PR title/body first, then the earliest commits and the shape of the original diff. Do not let later cleanup work redefine the PR thesis.

## Inventory Changes

Build a change inventory before recommending action. Group related changes by behavior, not just by file path.

For each group record:

- `id`: Stable short id.
- `title`: Human-readable cluster title.
- `files`: Important files touched.
- `why`: Confirmed or inferred reason the change was made.
- `evidence`: Commit messages, review comments, tests, code references, or diff context.
- `scope`: `in-scope`, `out-of-scope`, `revert/remove`, or `needs-decision`.
- `coupling`: Other groups that must ship with this group.
- `risk`: Correctness, security, migration, deploy, compatibility, or review risk.
- `suggested_destination`: Current PR, separate PR, revert, or user decision.

Use "confirmed" only when there is concrete evidence. Use "inferred" when reasoning from code shape or likely reviewer intent.

## Classify

Use these rules:

- Keep work in the current PR only when it directly supports the `scope_contract` or is required for the PR to build, test, or behave correctly.
- Mark work out of scope when it is valid but independently useful outside the PR thesis.
- Mark work revert/remove when it is wrong, speculative, unused, accidental, or only exists because the PR drifted.
- Mark work needs-decision when the code may be valuable but the product or ownership call is unclear.
- Do not call something out of scope merely because it is large. Size affects splitting, not validity.
- Do not keep a change in scope merely because it is already implemented.

## Cluster Out-of-Scope Work

Every valid out-of-scope change must belong to exactly one follow-up cluster.

Cluster rules:

- No catch-all follow-up PR.
- One cluster should be independently mergeable and reviewable.
- Merge clusters only when they are technically coupled and cannot safely ship apart.
- Split clusters when they touch different concerns, owners, rollout paths, migrations, APIs, or tests.
- Keep setup and usage together when separating them would break build or runtime behavior.
- Preserve dependencies between clusters rather than merging unrelated work.

Each follow-up cluster should have:

- Proposed branch name.
- Proposed PR title.
- One-line rationale for why it is separate.
- Files or commits it owns.
- Dependencies on other clusters.
- Verification needed.

## User Selection Gate

Before changing branches or moving code, present a cluster-level plan to the user.

Show:

- Current PR keep list.
- Out-of-scope follow-up clusters.
- Revert/remove candidates.
- Needs-decision items.
- Recommended default action.

Ask the user which clusters to address now. The user should choose clusters, not individual findings. Do not implement unselected clusters. Mark unselected clusters as deferred unless the user rejects or blocks them.

## Split Execution

Only execute after user approval.

When splitting:

1. Confirm the working tree is clean or that any dirty changes are intentional.
2. Preserve a backup reference to the original branch.
3. Create one branch per selected follow-up cluster from the correct base branch.
4. Move only that cluster's files/commits into its branch, using cherry-pick, patch application, or careful manual edits as appropriate.
5. Remove selected out-of-scope work from the current PR branch so it returns to the `scope_contract`.
6. Run relevant tests or validation on the current PR branch and each follow-up branch.
7. Push or open PRs only when the user has explicitly approved that action.

Prefer clear, reviewable commits over clever history surgery. If a clean split would require risky rewrite work, stop and present the safer options.

## Output

For an analysis-only run, return:

- The recovered `scope_contract`.
- A change inventory grouped by cluster.
- Why the review agent likely made each major change, with evidence labeled confirmed or inferred.
- Recommended current-PR contents.
- Proposed follow-up PR clusters.
- Revert/remove candidates.
- Questions requiring user decision.

For an executed split, return:

- Branches created or updated.
- Commits made.
- Which clusters went to which PR branch.
- What was removed from the original PR branch.
- Verification run and results.
- Remaining deferred or blocked clusters.
