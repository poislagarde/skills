---
name: revive-stale-pr
description: Picks up a pull request or branch that has sat untouched for a while. Checks whether the change is still needed against current main, brings the branch up to date and adapts it to upstream changes, and produces a step-by-step production rollout plan that flags every manual action before, during, and after deploy. Use when the user says it has been a while since they worked on a PR or branch, asks whether an old PR is still needed, wants a stale branch updated, or asks how to roll a change out to production.
---

# Revive Stale PR

Answer three questions about a branch the user has not touched in a while, in order. Stop early when the answer to the first makes the rest pointless.

1. Is this change still needed?
2. Does the branch still work on top of current main?
3. How does it get to production safely, and what has to be done by hand?

## 1. Still needed?

Recover what the PR was for from its title, description, linked issues, and earliest commits. Then look for evidence that the need has gone away or changed since:

- Main already contains the fix or feature, in the same or a different shape.
- The code, feature, or service it touches was removed or rewritten.
- The linked issue was closed, reprioritized, or superseded.
- Commits, comments, or docs on main show the team chose another approach.

Give a verdict: still needed, needed but different, or no longer needed. State the evidence and label anything inferred. If the verdict is "no longer needed" or "needed but different", stop and let the user decide before any merge work. Continue to step 2 only for "still needed", or when the user says to.

## 2. Bring it up to date

Use the `merge-origin-main` skill for the merge, conflict resolution, review, verification, and push. On top of that, look for upstream changes that affect the branch without a textual conflict: conventions adopted on main since, renamed or removed dependencies, changed configuration or deploy layout, reorganized tests, and features on main that now overlap with the PR. Adapt the branch so a reviewer reading it today sees code that belongs in the current repo.

If the PR has grown beyond its thesis while it sat, say so and offer the `split-overgrown-pr` skill instead of splitting it quietly.

## 3. Rollout plan

Derive the plan from the actual diff and the repo's deploy setup. Every step must trace back to something concrete in the change or the repo's deploy docs. Do not pad with generic advice.

Things that usually need a manual action; check each against the diff:

- Database migrations, backfills, and data fixes, including ordering relative to the code deploy and whether they are reversible.
- New or changed environment variables, secrets, and config, per environment.
- Feature flags: creation, default state, and who flips them.
- Third-party setup: webhooks, OAuth apps, DNS, API keys, vendor dashboards.
- Deploy ordering across services when one depends on another's new behavior.
- Caches, queues, or scheduled jobs that need draining, replaying, or a restart.
- What to watch after deploy, and how to roll back if it goes wrong.

Present the plan as ordered steps grouped into before, during, and after deploy. Mark each step automated or manual. For manual steps say who does it and in which system. Include the rollback path. This is a sensible default format; adapt it if the repo has its own release runbook.

## Report

Verdict on need with evidence; what changed in the branch to bring it current and what was verified; the rollout plan; open questions the user must answer before deploying.
