# Pull Request Description Guidelines

A reviewer who did not join the discussion should be able to tell why the PR exists, what behavior changes, which skills or repository components it affects, and how the result was checked. Keep the title and description aligned with the final implementation. Use a short description for a small change and add detail only where the change needs it.

## 描述语言

PR 描述必须使用中文，包括章节标题、正文、表格说明和检查清单。创建或修改已有 PR 描述时，都应遵守此要求。

文件路径、命令、API 端点、字段名、枚举值、产品名称和其他需要精确引用的技术标识保留原始拼写；其解释使用中文。保留实际验证结果和验证限制，不能因翻译而改变事实。

## 最终结果

PR 描述只写最终背景、行为变化、影响范围、验证结果和发布状态，不记录排查过程、调用重试经过、提交顺序或讨论历史。验证结果以最终实际检查为准；已经复测成功的项目写成功结果，仍未验证或未解决的限制应明确保留。

技能变更的背景应说明 Agent 原本在哪个判断或执行环节会出错，以及最终规则如何帮助它正确读取证据、解释结论和完成任务，不能只复述字段差异或罗列改动文件。

## What every PR should explain

- **Background and result:** Name the concrete problem and the behavior after the change. A short before/after example helps when a skill's answer or CLI behavior changes.
- **Scope and compatibility:** Name affected skills, shared contracts, scripts, tests, or repository files. Identify endpoint fields, command arguments, data structures, and callers when the PR changes them. Say whether existing skill installations or callers need to update; omit unrelated categories.
- **Changes by behavior:** Group changes by user-visible behavior or responsibility, rather than replaying commits or discussion history.
- **Validation:** Record checks actually run and their results, including relevant consistency tests and `scripts/sync-scripts.sh --check` when shared files change. State what was not checked, such as a live API response or installed ClawHub copy. Do not call a sampled check exhaustive.
- **Publication state:** Say whether the PR changes repository source only or also includes a separate publication step. A merge does not itself publish skills to ClawHub or create a GitHub Release. Name pending actions when they matter to use of the change.

## When the change warrants more detail

- For a skill contract or responsibility-map change, explain which module owns each new rule and how synced copies or dependent skills are affected.
- For API or CLI changes, describe relevant request/response fields, command allowlists, credit implications, and compatibility with existing callers. Include only the surfaces the PR actually touches.
- For a major upgrade or migration, explain the data flow and layer responsibilities, key design choices, old/new dependencies, migration order, caller impact, and rollback path. A small diagram may help.
- For a release PR or a PR that coordinates publication, distinguish merged source, manual `clawhub sync`, a GitHub Release tagged `*-release`, and the separate Lark notification. State the rollback or republish path that applies. See [release-notify.md](release-notify.md) for this repository's release flow.
- Mention backfills, deployments, or caller cutovers only if the PR actually involves them. Report each as completed, pending, or unverified; do not equate one state with another.

## Keep it readable and accurate

- Give each short paragraph one point. Use short lists for independent rules, conditions, null handling, exceptions, and pending work.
- Use a table for comparable field mappings, options, or costs. Use a short code block or diagram when a contract, structure, or formula needs exact notation.
- Keep key numbers near the result; link detailed logs and reports. Use readable units and suitable precision, leaving full precision in audit records.
- Separate completed facts, planned actions, and unverified hypotheses. Do not claim a skill is published or a caller has switched because the repository code changed.
- Omit discarded proposals, debugging steps, retry history, and discussion chronology. Explain the final design choices and replace vague claims such as “optimized” or “enhanced” with the behavior that changed.
- Remove inapplicable template prompts instead of filling the PR with empty sections.

These guidelines govern PR descriptions only. They do not change approval, commit, deployment, publication, or merge rules.
