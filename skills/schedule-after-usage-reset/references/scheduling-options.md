# Scheduling Options

## Choose the smallest supported scheduler

| Mode | Best for | Persistence | Skill action |
|---|---|---|---|
| Session cron | Work due later in the current Claude Code session | Session-scoped; unexpired tasks can return with `--resume` or `--continue` | Call `CronCreate`, then verify with `CronList` |
| Cloud routine | Work that must run with the terminal closed | Runs on Anthropic-managed infrastructure | Give the user an exact built-in `/schedule` command to invoke |
| Desktop scheduled task | Work requiring local files without an open CLI session | Managed by Claude Desktop | Explain the option; do not claim it was created |

Session cron uses the user's local timezone and a standard five-field cron
expression. One-shot tasks should be non-recurring. The session scheduler cannot
catch up for every missed interval and should not be presented as durable.

Cloud routines run autonomously. Their repository access, environment, network,
connectors, and branch permissions must be reviewed in Claude's routine setup.
Authentication remains inside the signed-in Claude product; this skill must not
handle account tokens.

## Authoritative references

- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)
- [Automate work with routines](https://code.claude.com/docs/en/web-scheduled-tasks)
- [Claude Code commands](https://code.claude.com/docs/en/commands)
