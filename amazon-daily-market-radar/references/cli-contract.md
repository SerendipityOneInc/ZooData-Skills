<!-- Canonical source - do not edit copies under amazon-* skill directories directly -->

# ZooData CLI Contract

## Ownership and application

This file owns the project-wide caller contract before and after every bundled `{skill_base_dir}/scripts/zoodata.py` invocation. Read it before selecting the first command, then apply it after each granular or composite result and before any additional API/tool call, fallback, state write, interpretation, or user-facing report.

It owns the shared invocation form, command-identity validation, execution-environment permission handling, caller/CLI responsibilities, composite-result reuse, result acquisition, transport-status precedence, terminal-interface classification, retry ownership, and partial-result handling. It does not own skill-specific command allowlists, endpoint request/response fields, business interpretation, scenario selection, conclusion authority, or any user-facing failure/report rendering.

## Invocation interface

1. Invoke the bundled client as `python {skill_base_dir}/scripts/zoodata.py [global options] <subcommand> [subcommand options]` using the active skill's local copy.
2. Place global options before the subcommand. Treat top-level and subcommand `--help` as the live invocation contract; help inspection makes no API request and consumes no credits.
3. Use the active skill to select the allowed workflow and command scope. Use this contract to validate and execute that selection; do not let this shared file select a business workflow.
4. Distinguish API/evidence commands from local-only diagnostic, prompt-rendering, and aggregation commands according to the selected subcommand's help. Do not attribute an API call or credit use to a local-only command.
5. Credential resolution is owned by the bundled CLI. Invoke it directly; do not inspect local credential stores or pre-resolve, compare, export, or override credential values in the caller.

## Command identity and composite reuse

1. Inspect the bundled CLI's top-level `--help` and the selected subcommand's `--help` before invocation. Execute only an exact literal subcommand exposed by the current client and allowed by the active skill.
2. Treat API endpoint identifiers and composite result keys as data identities, not CLI command names. Never derive a subcommand from either identity or invent an alias.
3. Treat a successful composite command's structured output as the evidence bundle for that run. Perform selection, narrowing, transformation, extraction, and formatting locally.
4. Do not make an additional API call solely to reread, reshape, or narrow evidence already present in the composite bundle.
5. A granular call after a composite is allowed only for evidence absent from the bundle when the active skill's workflow or an explicit non-terminal fallback requires it.
6. A keyword-driven composite resolves the working category through a fallback chain and records the outcome in `meta`: `meta.category_source` states how it resolved and `meta.resolved_category_path` carries the path used. An empty top-level `categories` section together with a non-null `meta.resolved_category_path` is successful fallback resolution (a multi-word product phrase not matching a category name), not missing data; read the resolved path and `category_source` before treating category evidence as absent.

## Execution-environment permission gate

Apply this gate before classifying a connection or network failure as a CLI/API interface failure.

1. Inspect the execution tool's permission profile and diagnostics. When they indicate, or strongly suggest, that a host sandbox or network policy blocked the request, treat the result as unresolved execution permission rather than endpoint failure.
2. Use the execution tool's permission or escalation mechanism to request access and rerun the exact unchanged CLI command. Do not first emit the skill's interface-failure notice or a succeeded/failed endpoint ledger.
3. A permission-approved rerun is environment recovery, not an external transport retry. Do not mutate the command, parameters, endpoint, or acquisition surface while requesting access.
4. If access is declined or no permission mechanism is available, state only that the required network access was not granted and the task could not continue. Do not label endpoints as failed or imply that API requests consumed credits when no request reached the service.
5. After the permission issue is resolved, classify the rerun normally through the sections below. Do not use this gate to bypass a returned HTTP status, credential failure, credit failure, validation failure, rate limit, or confirmed service outage.

## Result acquisition

1. By default, isolate every API/evidence command's complete stdout in a caller-owned raw-result file instead of streaming the full payload into the conversation. Use the hierarchy `<system-temp>/zoodata-results-<current-user-id>/<YYYY-MM-DD>/run-<secure-random>/`: the user root and date bucket are owner-only, each invocation gets a unique run directory, and no credential or subject value appears in a path.
2. Register cleanup before starting the CLI. Remove the task-owned `run-*` directory on normal completion, non-zero exit, projection failure, and interruption (`EXIT`, `HUP`, `INT`, and `TERM`, or the execution environment's equivalent `finally`). Delete the raw result as soon as classification and the validated projection are complete, then remove empty date and user-root directories when possible. As a backstop for untrappable termination or host failure, a new CLI process schedules a detached cleanup worker without waiting for it; scheduling occurs at most once per 24 hours. The worker parses only ISO-date directories in the current user's private ZooData root and silently removes whole date buckets older than 30 days. Cleanup or scheduling failure never blocks the requested command. Never retain a result as query state or delete another namespace, user, process, active task, non-date entry, or symlink. Only an explicitly authorized skill-owned persistent artifact, such as a monitoring baseline, may outlive the current run under that skill's separate storage contract.
3. Preserve the CLI process exit status. Always inspect stdout, even when the process exits non-zero, by reading the isolated raw-result file. Exit `1` with valid structured JSON means at least one API call failed; it does not make the JSON unreadable.
4. Parse and classify the complete raw payload before projecting it. For a success, locally emit only the claim-relevant fields plus the response identity, `_query`, coverage, and credit metadata required by the active skill. For a failure or partial result, retain the exact `success`, `error`, `_transport`, `_query`, partial-data, and credit signals needed by this contract. Projection is a local, zero-credit transformation and must never hide a failure, change a field's identity, or trigger a repeat API call.
5. Distinguish a collapsible transcript summary such as `… +N lines` from actual result loss. A fold whose full transcript remains readable is only a display affordance; inspect the isolated structured result and do not call the endpoint again. An explicit token-truncation marker, omitted middle, or incomplete displayed row set is likewise a conversation-rendering limit, not API evidence: re-project from the complete isolated raw file within the same run. A returned count such as `meta.total` does not prove that every row and required field was inspected. If the complete raw result is no longer available, suppress the completeness-dependent conclusion rather than inferring the omitted content.
6. Treat `_transport.status` as the authoritative outer HTTP status. Response-body or nested status-like fields never override it.
7. The CLI applies one fixed blind retry budget to every HTTP non-2xx or network failure. It does not assign HTTP-status meaning, select a status-specific workflow action, or vary retry behavior by status. Preserve the final non-2xx response body after those retries and never attach an earlier attempt's body to the final transport status. A structured JSON error remains the primary result with CLI-owned `success=false`, `_transport`, and `_query` metadata added; non-object JSON and non-JSON text remain available under explicit raw-response fields. Never replace a returned `error.code`, `error.message`, `error.details`, request ID, or replacement path with a generic CLI message.
8. For a composite payload, inspect nested endpoint results before classifying the whole workflow. Preserve returned `_query`, credit metadata, successful sections, and failure details internally.

## Classification order

After the execution-environment permission gate is resolved or found inapplicable, apply these routes in order:

1. Missing credentials before an evidence call follow the local skill's missing-key procedure.
2. `_transport.status=401` and `_transport.status=402` follow the local skill's credential and credit procedures. Do not retry externally, switch endpoints, or change credential sources after the CLI returns.
3. `_transport.status=422` is validation failure. Preserve the structured server error and `_query.params`; do not retry the unchanged request externally. Correct only fields identified by the server contract.
4. `_transport.status=410` is a retired-interface response. Do not retry externally, silently forward, mutate parameters, or derive a CLI command from the replacement path. Preserve and report the server's structured migration details. A replacement may be invoked only when it already maps to an exact literal subcommand in the current client's help and the active skill independently allows that route; otherwise stop the workflow and state that the installed skill/client must be updated.
5. `_transport.status=429` enters **Automatic rate-limit recovery** below. A rate limit is recoverable until that route reaches its stopping condition. `error.retryExhausted` describes the CLI's completed transport attempts, not the Agent's workflow disposition.
6. A terminal interface failure is present when the final result represents HTTP 404, HTTP 408, HTTP 5xx, exhausted non-HTTP transport failure after host permission restrictions have been ruled out or resolved, `MALFORMED_RESPONSE`, or non-zero execution without valid structured JSON. Rate-limit recovery that cannot safely continue also enters terminal handling.
7. A valid `status=empty` or a documented business/coverage error is not automatically terminal. A local skill fallback is allowed only when its contract explicitly supports that result and no terminal interface-failure signal is present.

## Automatic rate-limit recovery

The Agent owns this recovery inside the current authorized workflow. Waiting and resuming acquisition are execution details, not a new analysis stage or a user continuation choice. Do not end the turn, issue the terminal-failure notice, or ask whether to continue while recovery remains available.

1. Pause further ZooData evidence calls in the current workflow, including parallel callers under the Agent's control. Preserve compatible successful evidence, failed request identity, pending work, and returned credit metadata within the current run under **Result acquisition**; recovery does not authorize persistent query files or baseline writes.
2. Honor a valid server-provided cooldown or reset time when exposed in the result. Do not assume unavailable headers were returned. Without a usable cooldown, wait 60 seconds before the first recovery attempt, then 120 and 240 seconds for consecutive rate limits on the same request. A returned rate such as requests per minute is a pacing limit, not a retry delay. Use real waits, in chunks of at most 60 seconds, and respect cancellation.
3. Retry only the failed read request with its original endpoint, parameters, subject, period, filters, and page/cursor. Use the same acquisition surface and an exact allowed command whose help can express that request. Do not change credentials, substitute evidence, restart a successful page, or replay a whole partly successful composite. Apply **Composite and partial results** to recover its missing units.
4. After recovery, continue the pending acquisition and analysis automatically within the same authorized scope. Serialize subsequent calls and pace below the returned limit, accounting for known calls in its window across CLI invocations; the client's process-local pacing does not coordinate separate invocations. If no limit is exposed, start with at least 3 seconds between calls and increase spacing if throttling recurs. This interval is a conservative starting point, not a service quota or a guarantee against other clients using the account.
5. Allow at most three recovery invocations per failed request and at most 10 minutes of cumulative cooldown waiting in the current workflow, subject to any stricter user cost, call, or time boundary. Do not shorten a server cooldown to fit this budget. Reclassify every new response normally: success resumes work; another status follows its own route. Count returned usage across all invocations without counting composite totals twice; absent credit metadata does not mean a failed attempt was free.
6. Stop automatic recovery when those bounds are exhausted, the required wait exceeds the remaining budget, or the exact failed/pending request cannot be reconstructed and executed safely through an allowed command. Apply terminal handling and the local failure rendering, preserving the actual incomplete scope. Do not turn a persistent block into a repeated “continue?” menu or present partial evidence as a complete report. Recovery does not grant permission to exceed an explicit user budget.

## Retry and terminal behavior

The shared CLI owns the blind transport retry budget; the Agent owns all classification after the final result. Once the execution-environment permission gate is resolved or found inapplicable, a terminal interface failure requires:

1. Stop the current workflow turn. Do not retry externally, mutate parameters, switch endpoints or acquisition surfaces, start another tool command, or continue to a later workflow step.
2. Do not reinterpret an HTTP 5xx body as validation, credential, credit, empty coverage, or permission to try another date, subject, marketplace, filter, or page.
3. Retain earlier successful data for compatible later reuse, but do not produce the normal analysis, update monitoring/baseline state, or request the next workflow input.
4. Keep detailed messages, request parameters, retry logs, and control tokens internal unless the user explicitly requests diagnostics.
5. Hand off rendering to the active skill's local interface-failure template. This shared contract intentionally defines no user-facing wording.

## Composite and partial results

- A non-zero composite result may still contain successful sections. If any nested result is a terminal interface failure, stop after inventorying succeeded and failed interfaces; do not turn the surviving sections into the normal conclusion.
- Inspect actual nested transport results before interpreting composite abort metadata. `ABORTED_AFTER_TERMINAL_FAILURE` identifies work the CLI skipped, not another endpoint response; a 429 and its skipped dependents enter automatic recovery when no independent terminal failure is present. Recover the failed unit first, then execute only still-required skipped units whose original inputs can be established from the documented workflow and compatible results. Validate each granular command against the active allowlist and help. Keep an internal ledger of successful, failed, and unexecuted units; never rewrite the original composite as successful or infer missing query parameters from a result-key name.
- If all failures are documented non-terminal business/coverage failures, a local skill may use its explicit fallback and the compatible successful sections. Label coverage precisely and never present the composite as fully successful.
- Process exit status and JSON status must agree for a single-result command. A partial pagination failure must return `success=false` while preserving already collected rows under `data`.

## Realtime unavailable — offline fallback

`realtime/product` is a live scrape endpoint that can return a transient 200-success with an empty payload. Composites retry it a few times; if it is still empty, that item's result carries `_realtimeStatus="empty_after_retries"`, and the composite `meta` carries `realtimeUnavailable` (count) plus `realtimeFallbackHint`. When `realtimeFallbackHint` is present, tell the user realtime lookup is temporarily unavailable for those items, then continue the analysis using the offline snapshot data already gathered (products/search fields, history, price/BSR/rating). Do not stall, silently re-run, or fabricate the missing realtime detail.

## Partial review pagination

When `reviews-raw` fails after one or more successful pages, it returns `success=false`, preserves collected reviews and page count under `data`, and exposes the failed page request through `_failedQuery`. Never treat that payload as a complete review sample.

For a rate-limited paginated result, preserve successful pages and use the failed page identity (including `_failedQuery` when present) for recovery. Resume only if the allowed command exposes the exact page/cursor; failure metadata alone does not create a resume capability. If it does not, follow the recovery stopping condition rather than restarting pagination. Merge recovered pages only after checking query identity, order, duplicates, and the requested coverage boundary.
