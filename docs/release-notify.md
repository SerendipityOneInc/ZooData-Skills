# Production release → Lark notification

When ZooData-Skills is published to production, a "Launch Tracking" message is posted to
the **ZooData Launch Tracking Group** on Lark/Feishu. The message format (Chinese release
notes generated from the PR changelog, per-item source links and @mentions, rollback /
redeploy detection) is identical to hermes — both delegate to the same shared reusable
workflow `SerendipityOneInc/srp-actions/.github/workflows/release-notify-lark.yml`.

Workflow: [`.github/workflows/release-notify-lark.yml`](../.github/workflows/release-notify-lark.yml).

## How a release fires the notification

ZooData-Skills publishes its skills to ClawHub **manually** (`clawhub sync`). A production
release is marked by pushing a release **tag**, which triggers the notification:

```bash
# 1. Publish to production as usual
clawhub --dir . sync --all --owner apiclaw

# 2. Tag the released commit and push the tag
git tag zoodata-skills-v1.2.3-release
git push origin zoodata-skills-v1.2.3-release
```

The tag pattern is `zoodata-skills-v*-release`. Pushing it runs `release-notify-lark.yml`,
which resolves the tag/commit/actor and delegates to the shared reusable workflow to build
and send the Lark message. The changelog covers PRs merged since the previous
`zoodata-skills-v*-release` tag (first release ⇒ since the repo root commit).

## Manual run / testing (`workflow_dispatch`)

> `workflow_dispatch` only becomes available **after this workflow is on the default
> branch (`main`)** — GitHub does not expose the "Run workflow" button (or the
> `gh workflow run` API) for a workflow that exists only on a feature branch. So merge
> the PR first, then dispatch.

Run **Actions → Release notify (Lark) → Run workflow** with:

| Input | Default | Meaning |
|-------|---------|---------|
| `tag` | — (required) | An existing `zoodata-skills-v*-release` tag to (re)notify for |
| `dry_run` | `true` | Generate the release notes but **do not** send to Lark — use this to preview |
| `is_test` | `true` | Label the message as a test (`false` = manual resend of a real release) |

Recommended first run: `dry_run: true` to verify the notes render, then `dry_run: false`.

**A `dry_run: true` preview does not need the group configured** — `resolve` skips the
`LARK_CHAT_RELEASE_GROUP` fail-fast, and the Lark send is skipped, so
`LARK_CHAT_RELEASE_GROUP` and the `LARKSUITE_CLI_*` secrets are not required. It **does**
still run Claude release-notes generation, so the `APP_ID` / `APP_PRIVATE_KEY` /
`AWS_ROLE_TO_ASSUME` secrets must be available. A real send (`dry_run: false` or a tag
push) needs everything in the tables below.

To dispatch a dry-run against a throwaway tag:

```bash
git tag zoodata-skills-v0.0.0-release <some-commit> && git push origin zoodata-skills-v0.0.0-release
gh workflow run "Release notify (Lark)" -f tag=zoodata-skills-v0.0.0-release -f dry_run=true -f is_test=true
# inspect the run logs for the rendered release-notes.md, then delete the throwaway tag
git push origin :zoodata-skills-v0.0.0-release
```

## Configuration prerequisites (one-time, ops)

The workflow itself is committed, but it needs the following configured on the repo /
org before it can send. Until `LARK_CHAT_RELEASE_GROUP` is set, the `resolve` job
**fails fast** on purpose (rather than posting to the wrong group).

### Repository variables (Settings → Secrets and variables → Actions → Variables)

| Variable | Required | Value |
|----------|----------|-------|
| `LARK_CHAT_RELEASE_GROUP` | **yes** | The ZooData Launch Tracking Group `chat_id` (`oc_…`). Create the group if it does not exist and add the notifier bot to it. |
| `USER_MAPPING_JSON` | no | JSONL mapping GitHub login → Feishu `open_id` for @mentions. Empty ⇒ mentions degrade to literal `@login` text. |

### Inherited secrets (org or repo level; passed via `secrets: inherit`)

The reusable workflow needs the same secrets hermes uses. Ensure they are available to
ZooData-Skills (org-level secrets cover all repos; otherwise add them to this repo):

| Secret | Used for |
|--------|----------|
| `LARKSUITE_CLI_APP_ID` / `LARKSUITE_CLI_APP_SECRET` | Lark bot app credentials (mint tenant token, send the message). **The bot must be a member of the target group.** |
| `APP_ID` / `APP_PRIVATE_KEY` | GitHub App token for the Claude Code release-notes step |
| `AWS_ROLE_TO_ASSUME` | AWS OIDC role → Bedrock (Claude generates the notes) |

## Notes

- **No ClawHub key in CI.** Publishing stays a manual `clawhub sync`; this workflow only
  *notifies* on the release tag. It never handles the ClawHub API key.
- **Baseline detection degrades gracefully.** ZooData-Skills has no k8s deploy workflow;
  the reusable falls back from deploy-run history → previous release tag → repo root
  commit, so the changelog range is always well-defined.
- To change the message format, update the shared reusable in `srp-actions` — both hermes
  and ZooData-Skills pick it up.
