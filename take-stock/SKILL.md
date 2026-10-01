---
name: take-stock
description: Takes stock of the current session so far, covering what was done, the verified status of each item, and step-by-step instructions for the next steps. Use when the user types /take-stock, asks for a recap, where things stand, or what has been done so far, wants to make sure nothing was dropped, or wants a handoff summary before stepping away.
---

# Take Stock

Take stock of this session in a report that someone picking it up cold could act on: what was done, where each item stands, and the next steps in order. Taking stock is read-only. Gather and report; leave files, branches, and processes as they are.

## Gather

Walk the session from the first request onward. Every request the user made becomes an item, including ones that were deferred, dropped, or replaced by a later request. Side findings worth acting on become items too.

Check status against the environment, not memory: working tree, branch, commits and whether they are pushed, PR and CI state, files written, processes left running. An item is verified only if its evidence was seen this session (a test run, a command's output) or is checked now. If earlier context was summarized, re-check what the summary claims.

## Status

Give each item exactly one status:

- **done**: finished and verified; cite the evidence.
- **unverified**: finished but never checked; name the missing check.
- **in progress**: partly done; say what remains.
- **blocked**: waiting on something; name it and who can unblock it.
- **not started**: requested but not begun.
- **dropped**: deliberately not done; say why and who decided.

## Next steps

Number the steps in the order they must happen, ending where the user's goal is met. Each step is one concrete action: the exact command, file, or decision, and who does it (agent or user). Flag manual actions and decisions only the user can make. Ideas beyond the goal go in a short follow-ups list after the steps.

## Report

Default format; adapt it to the session:

1. **Items**: one line each with its status.
2. **Current state**: branch, uncommitted changes, unpushed commits, open PRs, anything left running.
3. **Next steps**: the numbered list, then follow-ups.
4. **Open questions**: decisions the user owes, if any.
