---
name: fork-herdr
description: Forks the current session into a new herdr tab, where the fork works on a side issue in its own git worktree while this session carries on with the main task. Use when the user types /fork-herdr, or asks to fork this session, spin off a tangent, or hand a side issue to a parallel session in a worktree.
---

# Fork into a herdr Tab

Hand the side issue in the skill's arguments to a fork of this session: same conversation history, new session ID, its own worktree, in a new herdr tab next to this one. This session keeps its own direction.

## Steps

1. If the arguments are empty, ask for the side issue. If `HERDR_WORKSPACE_ID` or `CLAUDE_CODE_SESSION_ID` is unset, stop and say which: the skill needs a Claude Code session running inside herdr.
2. Pick a short kebab-case slug for the side issue that `git worktree list` does not already use. It names the worktree (`.claude/worktrees/<slug>`), its `worktree-<slug>` branch, the tab, and the forked session.
3. Open the tab and launch the fork in one shell call, pasting the arguments verbatim into the heredoc. The prompt travels as a tab environment variable, so the command typed into the pane stays free of user text and the pane's interactive shell cannot mangle it:

   ```bash
   slug=<slug>
   prompt=$(cat <<'FORK_HERDR_PROMPT'
   You are a fork created by fork-herdr. The original session continues the main task; work only on the issue below and do not fork again.

   <arguments, verbatim>
   FORK_HERDR_PROMPT
   )
   pane=$(herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" --label "$slug" --no-focus --env "FORK_HERDR_PROMPT=$prompt" | jq -r .result.root_pane.pane_id)
   herdr pane run "$pane" "claude --resume $CLAUDE_CODE_SESSION_ID --fork-session -w $slug -n $slug \"\$FORK_HERDR_PROMPT\""
   ```

4. Report in one line: the tab label and the worktree path. End the turn there. The side issue belongs to the fork now; this session picks up its own work on the user's next message.
