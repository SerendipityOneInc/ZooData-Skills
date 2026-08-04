# Production release → Lark notification

When ZooData-Skills is released to production, a "Launch Tracking" message is posted to the
**ZooData Launch Tracking Group** on Lark/Feishu, with the same format hermes uses (Chinese
release notes generated from the PR changelog, source links, @mentions, rollback/redeploy
detection).

## Why the notification does NOT run in this repo

ZooData-Skills is a **public** repo. The release-notify secrets (Lark bot, GitHub App, AWS
Bedrock role) are org secrets that are — correctly — **not exposed to public repos**. So this
repo does not (and should not) run the notification itself.

Instead, **`hermes-workspace` (internal, which already has those secrets) runs the
notification on this repo's behalf**, via the shared reusable's `source_repo` input. The
reusable checks out ZooData-Skills (public, readable with the default token) and builds the
changelog from this repo's history. **No notification credential ever lives in this public
repo.**

Moving parts:
- `srp-actions/.github/workflows/release-notify-lark.yml` — shared reusable; `source_repo`
  input lets it notify for a repo it does not run in.
- `hermes-workspace/.github/workflows/zoodata-skills-release-notify.yml` — the manual
  caller that runs it for ZooData-Skills.

## Release flow

```bash
# 1. Publish to ClawHub (manual, as today; the ClawHub key stays local)
clawhub --dir . sync --all --owner apiclaw

# 2. Cut a GitHub Release whose tag ends in -release
gh release create v1.3.0-release --title "v1.3.0 — <headline>" --notes "..."
```

Then, to send the Lark notification:

```
# 3. In hermes-workspace: Actions → "ZooData-Skills release notify" → Run workflow
#    tag = v1.3.0-release,  dry_run = true (preview) → then dry_run = false (send)
```

Step 3 is a **manual** action in hermes-workspace (no polling). Do a `dry_run: true` run
first to preview the rendered notes, then `dry_run: false` to send.

### Tag convention: the tag must end in `-release`

The reusable matches the previous production release by a `release$` tag suffix, so release
tags must be `v*-release` (e.g. `v1.3.0-release`), not the bare `v1.2.2` this repo used
historically. The changelog covers PRs merged since the previous `v*-release` tag; the first
release under this convention falls back to the repo root commit (a one-time full history).

## One-time configuration (ops)

Done in **hermes-workspace / srp-actions**, not here:

| Where | What |
|-------|------|
| srp-actions | reusable with the `source_repo` input (PR: "add optional source_repo") |
| hermes-workspace | the `zoodata-skills-release-notify.yml` caller workflow |
| hermes-workspace repo var | `LARK_CHAT_ZOODATA_RELEASE` = ZooData Launch Tracking Group `chat_id` |
| hermes-workspace secrets | the existing release-notify secrets (already present); the Lark bot must be a member of the target group |

Nothing needs to be configured in this (public) repo.
