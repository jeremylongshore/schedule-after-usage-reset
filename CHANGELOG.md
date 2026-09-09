# Changelog

All notable changes to this project are documented here.

## [2.0.0] - 2026-09-09

### Changed

- Replace direct Keychain credential extraction and the undocumented usage API
  with Claude Code's supported one-shot cron tools and built-in `/schedule`
  routine workflow.
- Require the reset timestamp to be user-visible or explicitly supplied.
- Add scheduler verification, persistence guidance, and failure receipts.
- Update repository and installation metadata after the public repository move.
- Add a deterministic CI gate for version, catalog, and safety-contract drift.

### Security

- The skill no longer reads, stores, or forwards Claude OAuth credentials.

## [1.0.0]

- Initial release by lemondepat.
