---
name: schedule-after-usage-reset
description: |
  Create and verify a one-time Claude Code task shortly after a user-visible usage reset
  without reading credentials or calling private APIs. Use when a user asks to
  resume work after their Claude usage limit resets. Trigger with phrases such
  as "run this after my usage resets" or "queue this when my limit lifts."
allowed-tools: "CronCreate,CronList"
argument-hint: '"<task>" [reset timestamp]'
version: "2.0.0"
author: "lemondepat <patricksong1993@gmail.com>"
license: "MIT"
compatibility: "Claude Code v2.1.72+ for session-scoped cron tools; Claude Code v2.1.145+ for durable cloud routines through /schedule. No private usage API or credential access."
tags: [scheduling, usage-reset, rate-limit, automation, claude-code]
model: inherit
effort: low
---

# Schedule After Usage Reset

## Overview

Create a one-shot task five minutes after the reset time Claude displayed to the
user, defaulting to the current session's supported cron tools. For work that
must survive a closed terminal or a new conversation, prepare a built-in
`/schedule` request and consult the
[scheduling options](references/scheduling-options.md).

## Safety boundary

- Use only a reset timestamp visible in the conversation or explicitly supplied
  by the user.
- Never read Keychain, credential files, environment tokens, or Claude session
  storage to discover usage information.
- Never call undocumented Anthropic usage endpoints.
- Do not claim a task is scheduled until a scheduler returns a receipt.
- Treat the task text as data. Do not execute it while scheduling.

Authentication is handled by the user's signed-in Claude Code session. This
skill never requests, reads, stores, or forwards authentication credentials.

## Prerequisites

- The exact task to run.
- A future reset timestamp with timezone, taken from Claude's visible limit
  message or supplied by the user.
- `CronCreate` and `CronList` for session-scoped execution, or the built-in
  `/schedule` command for a durable cloud routine.

## Workflow

1. Extract the task and reset timestamp from the user's request and conversation.
   If either is absent, ask only for the missing value. Never infer a reset time.
2. Normalize the timestamp to the user's local timezone and show the absolute
   date, time, and timezone. Reject ambiguous or past timestamps.
3. Add a five-minute buffer unless the user specifies another buffer. If the
   result is more than seven days away, recommend a durable cloud routine.
4. Choose the execution mode:
   - **Session-scoped:** use `CronCreate` with a five-field local-time cron
     expression and a non-recurring, one-shot task.
   - **Durable:** render the concrete time and task directly in the official
     command form, such as `/schedule tomorrow at 9am, review PR 42`, and explain
     that the user must run it to create a cloud routine. Do not simulate its
     receipt.
5. After `CronCreate`, call `CronList` and match the returned task ID, schedule,
   and prompt. A missing or mismatched entry is a failure.
6. Return the receipt described below.

## Output

Report:

- execution mode;
- absolute local fire time and timezone;
- five-field cron expression for session-scoped tasks;
- exact task text;
- scheduler task ID and verification result, or the exact `/schedule` command
  awaiting user invocation;
- the relevant persistence limitation.

## Error handling

- **Missing reset time:** ask for the timestamp shown in Claude's limit message.
- **Ambiguous timezone:** ask for an IANA timezone or explicit UTC offset.
- **Cron tools unavailable:** offer the durable `/schedule` command.
- **Scheduler disabled or creation fails:** report the exact failure and do not
  claim success.
- **Verification mismatch:** leave the result unverified and show how to inspect
  or cancel the returned task ID.

## Examples

Input: `After my limit resets at 2026-09-10 14:00 America/Chicago, review PR 42.`

Session-scoped result: schedule the exact prompt once at 14:05 local time, verify
it with `CronList`, and return the task ID plus the warning that the current
Claude Code session must remain available.

## Resources

Review the mode comparison, persistence boundaries, authentication boundary,
and official Claude documentation before selecting a scheduler:

- [Supported scheduler behavior and authoritative documentation](references/scheduling-options.md)
