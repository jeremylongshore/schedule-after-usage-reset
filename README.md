# schedule-after-usage-reset

A Claude Code skill for safely queueing a one-time task shortly after a visible
usage-limit reset. It uses Claude Code's supported scheduler surfaces and never
extracts account credentials or calls private usage APIs.

## What it does

When you say “run this after my usage resets,” the skill:

1. reads the reset timestamp from the conversation or asks you to provide it;
2. adds a five-minute safety buffer;
3. creates and verifies a session-scoped one-shot task with Claude Code's cron
   tools, or prepares a built-in `/schedule` command for a durable cloud routine;
4. returns a receipt with the exact task, time, mode, and persistence limits.

The skill does not inspect macOS Keychain, local credential files, environment
tokens, or undocumented Anthropic endpoints.

## Installation

### Claude Code plugin

```text
/plugin marketplace add jeremylongshore/schedule-after-usage-reset
/plugin install schedule-after-usage-reset@lemondepat
```

Reload plugins after installation if Claude Code requests it.

### Agent Skills CLI

```bash
npx skills add jeremylongshore/schedule-after-usage-reset --skill schedule-after-usage-reset
```

### Manual

Copy `skills/schedule-after-usage-reset/` into your agent's skills directory.

## Requirements

- Claude Code v2.1.72 or later for session-scoped cron tools.
- Claude Code v2.1.145 or later for durable cloud routines through `/schedule`.
- A reset timestamp displayed by Claude or explicitly supplied by the user.

Session-scoped tasks only fire while the session is available. Use a cloud
routine or Claude Desktop scheduled task when the work must survive a closed
terminal.

## Attribution

Created by lemondepat (Patrick Song). Maintained in the public
[`jeremylongshore/schedule-after-usage-reset`](https://github.com/jeremylongshore/schedule-after-usage-reset)
repository.

## License

MIT
