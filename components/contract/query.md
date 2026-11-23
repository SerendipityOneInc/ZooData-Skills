# WorkBuddy MCP acquisition

## Select tools and construct requests

1. Use only connected, read-only MCP tools within the Skill's declared capabilities. Capability paths identify the required reads; resolve the actual callable names from the connected tools.
2. Before first use, read the connected tool's description and schema. Reuse that definition within the session unless the tool changes or an error requires checking it again. Construct supported date, marketplace, batch, filter and paging inputs, including their types and defaults.
3. Interpret returned fields using the current interface definition when domain notes differ. If a required definition is unavailable, preserve the returned value without guessing a conclusion that depends on its meaning.
4. Before a dependent data query, check that each requested object is explicitly within the user's scope or uniquely resolved from the context. If a lookup leaves several possible subjects, confirm the intended subject before querying their data; a list of matches is not a user-selected comparison set.

## Choose the appropriate evidence level

1. Start with the selected task's profiles, trend indicators and supporting observations. If they already contain the measures needed by the question, do not query details merely to recalculate those measures.
2. Query details for an unresolved upper-level question or an explicit request for records, fields or raw series.
3. If no matching upper-level indicator exists, use the task's documented primary source.

## Select the trend period

1. Honor the period, end date and granularity in the question. If only the period length is unspecified, request **6 months for monthly trends, 3 months for weekly trends, and 1 month for daily trends**. Use completed periods through the requested cutoff or latest available complete observation unless the user asks for a partial period.
2. Pass the supported start/end or window explicitly when the API default differs. For weekly and daily series use observations in the corresponding calendar-month lookback. If only preset windows are supported, select the closest supported window and state its actual length. Respect source coverage and budget, and identify a shorter available period. On an authorized retry, keep the original trend period. Reuse partial results and request only the uncovered months within budget. If the period remains incomplete, label the coverage gap.

## Apply sorting and pagination

1. Select a supported sort field and direction from the user's requested order or the domain method's default. A domain default is an ordering requirement. Pass the corresponding sort inputs unless the schema documents exactly the same default order. When neither the user nor the domain method requires an order, omit sort inputs and use the documented API default; if undocumented, label the order unspecified.
2. Keep subjects, periods, filters and sorting inputs unchanged across pages of the same query.
3. For a list request without a specified count or exhaustive scope, start with 20 records when supported by the tool. Continue only for coverage needed by the question. Explicit user coverage and tool constraints take precedence; do not describe an initial page as complete coverage.

## Reuse responses and record usage

1. Before a new query, reuse responses that meet the current subject, marketplace, period, filter and metric-definition requirements. Query only the missing data.
2. Keep every query within the user's coverage and cost limits. If a limit prevents a required read, stop that read and identify the data not obtained.
3. Inspect the complete structured response, including records omitted from previews. For large responses available as files, process all relevant records locally and bring only the fields, summaries or selected rows needed for the question into the reasoning context. Keep the original file and identifiers for follow-up reads instead of printing the entire JSON again. Retain the source tool, request conditions, actual order, original row order, batch-item identities and statuses, and returned usage.
4. If the host denies access to a saved response, respect the denial. Use already accessible structured results for the same request. If they are incomplete, deliver supported findings and identify the missing business result. Keep file permissions, paths, and batching decisions out of user questions. Never replay a successful paid request just to change the response size.
5. For a large multi-object read without an agreed budget, estimate the cost of the remaining work from the tool’s billing unit and the scoped objects or requests. Confirm the research scope and estimated credits once before spending. Reuse existing approval within its limit. If a necessary estimate is unavailable, ask for a spending cap and proceed only when it can be enforced.
6. Record usage only from returned metadata. Do not invent missing values or add totals to their component amounts.

## Handle authentication and private inputs

1. Use the connector's authentication flow. Do not request credentials in ordinary chat or include them in query parameters, messages or output files.
2. Send only documented query inputs. Keep seller costs and private reports in the analysis context unless the selected tool requires them and the user has authorized their transmission.

## Handle failed or empty results

1. If the connection is unavailable, credentials are rejected or credits are exhausted, stop the affected read. State the reason and missing business result. Deliver findings supported by existing data and identify the smallest useful seller input if it can fill the gap. With no data, explain in chat. Do not estimate a top-up or guarantee completion.
2. Correct invalid parameters only when the returned error and current schema determine the correction; otherwise stop and identify the missing request information.
3. Retry rate limits or temporary failures only under explicit connector retry rules and host and cost limits. Stop if those rules are absent or a limit is reached; do not replay successful pages.
4. Treat a valid empty result as no matches under the current query conditions, not as an error to retry.
5. After a read fails, continue necessary reads that do not depend on it. Retain successful results and identify the incomplete part.
