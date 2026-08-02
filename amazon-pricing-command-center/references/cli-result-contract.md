<!-- Canonical source - do not edit copies under amazon-* skill directories directly -->

# ZooData CLI Result and Interface Failure Contract

## Ownership and application

This file owns the project-wide caller contract for every bundled `{skill_base_dir}/scripts/zoodata.py` invocation. Apply it after each granular or composite command and before any additional API/tool call, fallback, state write, interpretation, or user-facing report.

It owns CLI-result acquisition, transport-status precedence, terminal-interface classification, retry ownership, and partial-result handling. It does not own endpoint request/response fields, business interpretation, scenario selection, conclusion authority, or any user-facing failure/report rendering.

## Result acquisition

1. Always inspect stdout, even when the process exits non-zero. Exit `1` with valid structured JSON means at least one API call failed; it does not make the JSON unreadable.
2. Treat `_transport.status` as the authoritative outer HTTP status. Response-body or nested status-like fields never override it.
3. For a composite payload, inspect nested endpoint results before classifying the whole workflow. Preserve returned `_query`, credit metadata, successful sections, and failure details internally.

## Classification order

Apply these routes in order:

1. Missing credentials before an evidence call follow the local skill's missing-key procedure.
2. `_transport.status=401` and `_transport.status=402` follow the local skill's credential and credit procedures. Do not retry or switch endpoints.
3. `_transport.status=422` is validation failure. Preserve the structured server error and `_query.params`; do not retry the unchanged request. Correct only fields identified by the server contract.
4. A terminal interface failure is present when the result carries `error.action="STOP_CURRENT_TURN. APPLY_SKILL_INTERFACE_FAILURE_TEMPLATE. DO_NOT_SELECT_ANOTHER_COMMAND."`, or represents exhausted HTTP 5xx, exhausted 429, exhausted non-HTTP transport failure, endpoint unavailability, `MALFORMED_RESPONSE`, or non-zero execution without valid structured JSON.
5. A valid `status=empty` or a documented business/coverage error is not automatically terminal. A local skill fallback is allowed only when its contract explicitly supports that result and no terminal interface-failure signal is present.

## Retry and terminal behavior

The shared CLI owns transport retries. On a terminal interface failure:

1. Stop the current workflow turn. Do not retry externally, mutate parameters, switch endpoints or acquisition surfaces, start another tool command, or continue to a later workflow step.
2. Do not reinterpret an HTTP 5xx body as validation, credential, credit, empty coverage, or permission to try another date, subject, marketplace, filter, or page.
3. Retain earlier successful data for compatible later reuse, but do not produce the normal analysis, update monitoring/baseline state, or request the next workflow input.
4. Keep detailed messages, request parameters, retry logs, and control tokens internal unless the user explicitly requests diagnostics.
5. Hand off rendering to the active skill's local interface-failure template. This shared contract intentionally defines no user-facing wording.

## Composite and partial results

- A non-zero composite result may still contain successful sections. If any nested result is a terminal interface failure, stop after inventorying succeeded and failed interfaces; do not turn the surviving sections into the normal conclusion.
- If all failures are documented non-terminal business/coverage failures, a local skill may use its explicit fallback and the compatible successful sections. Label coverage precisely and never present the composite as fully successful.
- Process exit status and JSON status must agree for a single-result command. A partial pagination failure must return `success=false` while preserving already collected rows under `data`.

## Partial review pagination

When `reviews-raw` fails after one or more successful pages, it returns `success=false`, preserves collected reviews and page count under `data`, and exposes the failed page request through `_failedQuery`. Never treat that payload as a complete review sample.
