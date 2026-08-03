# Claude Code Repository Instructions

Before modifying or reviewing any skill, read and follow
`CONTRIBUTING.md`, especially `Skill Specification Ownership`, then read the
affected skill's `SKILL.md` and review its modules against the responsibility
map declared there. Run the relevant consistency tests before completing the
change.

## Releasing / publishing

Skills are published to ClawHub **manually** via `clawhub sync` (the ClawHub key stays
local — never in CI). A release is a repo-level milestone cut as a GitHub Release whose
tag ends in `-release` (e.g. `v1.2.3-release`); publishing that Release fires the Lark
launch-tracking notification. See `docs/release-notify.md`.

Keep this file as an instruction bridge. Do not copy skill-specific contracts,
module policies, or runtime rules into it.
