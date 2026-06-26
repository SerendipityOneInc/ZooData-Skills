# Web Extract — Endpoint Reference (ZooData WebTools API)

Full request/response schemas for every endpoint under `/openapi/v2/webtools/*`.
Load this file when you need exact field names, error codes, billing rules, or response shapes — the SKILL.md is the day-to-day cheat sheet, this is the source of truth.

**Base URL**: `https://api.zoodata.ai/openapi/v2/webtools`
**Auth**: `Authorization: Bearer hms_live_xxx`
**Content-Type**: `application/json` (all POSTs)

---

## Common Response Envelope

Every endpoint returns this shape:

```json
{
  "success": true,
  "data": { /* endpoint-specific payload */ },
  "error": null,
  "meta": {
    "requestId": "req_xxx",
    "timestamp": "2026-06-26T07:00:00Z",
    "creditsRemaining": 1000,
    "creditsConsumed": 1.0,
    "creditsRemainingExact": 1000.0,
    "creditsConsumedExact": 1.0
  }
}
```

On failure, `success: false`, `data: null`, and `error` is populated:

```json
"error": {
  "code": "ACCESS_DENIED",
  "message": "Page refused the request",
  "details": { "statusCode": 403 }
}
```

### Error codes

| Code | When it happens | Billed? |
|---|---|---|
| `ACCESS_DENIED` | Target returned 401/403/429/451/503 — anti-bot block | ❌ No |
| `RATE_LIMITED` | Target returned 429 to us | ❌ No |
| `UNREACHABLE` | DNS resolution failed | ✅ Yes |
| `TIMEOUT` | Took longer than SLA | ✅ Yes |
| `CONTENT_UNAVAILABLE` | Generic fetch failure | ✅ Yes |
| `INVALID_REQUEST` | Schema validation failed → 422 | ❌ No (4xx before work) |
| `NOT_FOUND` | Unknown crawl job_id (or wrong tenant) | ✅ Yes (1 credit per poll) |
| `UPSTREAM_TIMEOUT` | Internal pipeline timeout | ❌ No |
| `UPSTREAM_RATE_LIMITED` | Our infra throttle | ❌ No |

HTTP-layer status codes that the API returns directly (not wrapped in the envelope):

| Status | Meaning |
|---|---|
| `401 Unauthorized` | API key invalid / revoked / expired |
| `402 Payment Required` | Account out of credits |
| `429 Too Many Requests` | Per-key RPM or concurrency cap hit — honor `Retry-After` header |

---

## 1. `POST /scrape` — Scrape a single URL

**Purpose**: Pull one URL through a headless browser, return content in chosen format(s).
**SLA**: 120s.
**Billing**: 1 credit per call (refused requests not billed).

### Request

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `url` | string | ✅ | — | Full URL with scheme |
| `formats` | string[] | ❌ | `["markdown"]` *(API default)* | Any of `markdown`, `json`, `rawHtml`. Max 3. Output order matches request order. **This skill's convention is to always pass `["json"]` explicitly** unless the user asks for prose (markdown) or DOM (rawHtml) — see SKILL.md for the rationale. |

### Response (`data`)

| Field | Type | When present | Notes |
|---|---|---|---|
| `url` | string | always | Echo of request URL |
| `markdown` | string | when `markdown` in formats | Boilerplate-stripped article text |
| `json` | object | when `json` in formats | Structured extraction (page_type + page-specific fields like title/price/author/publishedAt) |
| `rawHtml` | string | when `rawHtml` in formats | Post-render DOM HTML |
| `meta` | object | always | `statusCode`, `title`, `description`, `sourceUrl`, `language`, `contentType` |

**⚠️ Always check `data.meta.statusCode`.** A `success: true` response can still contain an error page (404/500) from the target.

---

## 2. `POST /scrape-interactive` — Scrape after browser actions

**Purpose**: Drive a headless browser through a sequence (click, type, scroll, JS, wait), then scrape.
**SLA**: 180s.
**Billing**: 1 credit per call.

### Request

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `url` | string | ✅ | — | Initial URL to load |
| `actions` | object[] | ✅ | — | Max 50 actions. Cumulative `wait` ≤ 60,000 ms. |
| `formats` | string[] | ❌ | `["markdown"]` *(API default)* | Same as `/scrape` — skill defaults to `["json"]`. |

### Action types

| Type | Required fields | Notes |
|---|---|---|
| `wait` | `milliseconds` (int) | Throttled — total across all `wait`s ≤ 60s |
| `click` | `selector` (CSS) | Triggers a click event |
| `write` | `selector`, `text` | Types text into the element |
| `press` | `key` | Keyboard key (e.g. `Enter`, `Tab`, `Escape`) |
| `scroll` | `direction` (`up`/`down`), `amount` (int) | `amount` is page heights |
| `scrape` | — | Captures the page state at this point in the sequence |
| `executeJavascript` | `javascript` (string) | Return value is captured |

Response shape: same as `/scrape`.

---

## 3. `POST /search` — Web search (two modes)

**Purpose**: Google-style web search. Returns SERP results; optionally deep-scrapes each.
**SLA**: 120s.
**Billing**:
- SERP-only (no `scrapeOptions`): 1 credit min (empty result set still 1)
- Deep-scrape: `max(1.0, result_count)` — up to ~20 for `limit=20`
- Handler pre-checks balance against worst case (limit × 1.0) before any work

### Request

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `query` | string | ✅ | — | Supports Google operators inline (`site:`, `-`, `"…"`, `intitle:`, `filetype:`) |
| `limit` | int | ❌ | 10 | Range 1–20 |
| `sources` | string[] | ❌ | `["web"]` | Subset of `web`, `news`, `images` (combinable) |
| `tbs` | string | ❌ | — | Time filter: `qdr:d` (day), `qdr:w` (week), `qdr:m` (month), `qdr:y` (year) |
| `includeDomains` | string[] | ❌ | — | Max 20. **Bare hostnames only** (e.g. `python.org`) — folded into `site:` operators |
| `excludeDomains` | string[] | ❌ | — | Max 20. Bare hostnames only. Folded into `-site:` operators |
| `scrapeOptions` | object | ❌ | — | Presence triggers deep-scrape. Omit for SERP-only. |
| `scrapeOptions.format` | string | ❌ | `markdown` | `markdown` or `json` |

**Domain folding** (the API echo-protects this — the caller never sees the augmented query):
- `includeDomains=["a.com","b.com"]` → query gets ` (site:a.com OR site:b.com)` appended
- `excludeDomains=["spam.com"]` → query gets ` -site:spam.com` appended
- Domain validation: must be a clean FQDN. Anything with scheme/path/whitespace/operator chars → 422.

### Response (`data`)

| Field | Type | Notes |
|---|---|---|
| `query` | string | The **original** user query (not augmented) |
| `results` | object[] | One per SERP entry |

Each result:

| Field | Type | When | Notes |
|---|---|---|---|
| `url` | string | always | Result URL |
| `meta.title` | string | always | Page title |
| `meta.description` | string | usually | SERP snippet |
| `meta.source` | string | always | `web`, `news`, or `images` |
| `meta.publishedAt` | string | news | ISO 8601 |
| `meta.imageUrl` | string | images | Direct image URL |
| `meta.statusCode` | int / null | deep-scrape only | The scraped page's HTTP status |
| `markdown` | string | deep-scrape with `format=markdown` | |
| `json` | object | deep-scrape with `format=json` | |

**Deep-scrape gotcha**: `results.length` may be less than `limit`. Results with no content in the chosen format are dropped.

---

## 4. `POST /map` — Discover URLs from a website

**Purpose**: Enumerate URLs reachable from a seed (sitemap + shallow crawl).
**SLA**: 90s.
**Billing**: 1 credit per call (regardless of URL count returned).

### Request

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `url` | string | ✅ | — | Seed URL |
| `limit` | int | ❌ | 5000 | Range 1–100000 |
| `search` | string | ❌ | — | Max 500 chars. Ranks results by relevance to this keyword. |
| `sitemapMode` | string | ❌ | `include` | `include` (sitemap + crawl), `only` (sitemap exclusive), `skip` (crawl only) |
| `includeSubdomains` | bool | ❌ | `true` | If false, restrict to seed host only |
| `includePaths` | string[] | ❌ | — | Max 50 patterns, each ≤500 chars. **Regex** (e.g. `/blog/.*`) |
| `excludePaths` | string[] | ❌ | — | Max 50 patterns, each ≤500 chars. Regex. |
| `ignoreQueryParameters` | bool | ❌ | `true` | If true, `?a=1` and `?a=2` collapse into one URL |

### Response (`data`)

```json
{
  "url": "https://www.python.org",
  "links": [
    {"url": "...", "title": "...", "description": "..."}
  ]
}
```

---

## 5. `POST /crawl` — Submit async recursive crawl job

**Purpose**: Start a recursive crawl. Returns a `job_id`; pages are fetched in background.
**SLA**: 10s (submission only).
**Billing**: 1 credit per submit (NOT per page).

### Request

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `url` | string | ✅ | — | Seed URL |
| `limit` | int | ❌ | 100 | Range 1–10000. Page budget. |
| `maxDepth` | int | ❌ | — | Range 1–10 |
| `includePaths` | string[] | ❌ | — | Regex, max 50 |
| `excludePaths` | string[] | ❌ | — | Regex, max 50 |
| `allowSubdomains` | bool | ❌ | `false` | Follow links to subdomains |
| `sitemapMode` | string | ❌ | `include` | Same as `/map` |
| `ignoreQueryParameters` | bool | ❌ | `false` | **Note: opposite default from `/map`** |
| `crawlEntireDomain` | bool | ❌ | `false` | If true, ignore path-of-seed-URL restriction |

### Response (`data`)

```json
{
  "id": "job_abc123xyz",
  "url": "https://example.com"
}
```

`id` matches pattern `^[A-Za-z0-9_-]{1,64}$` and is bound to your API key tenant.

---

## 6. `GET /crawl/{job_id}` — Poll crawl job status

**Purpose**: Fetch already-completed pages from a running or finished crawl.
**SLA**: 10s.
**Billing**: 1 credit per successful poll. `NOT_FOUND` (warmup or expired) returns `success:false` and is **not charged**.

### Path & query

| Param | Type | Required | Default | Notes |
|---|---|---|---|---|
| `job_id` (path) | string | ✅ | — | From `/crawl` submit |
| `skip` (query) | int | ❌ | 0 | Pagination offset into `data.data[]` |
| `limit` (query) | int | ❌ | all | Range 1–1000 |

### Response — `data` is an object (NOT an array; pages are nested at `data.data`)

```json
{
  "success": true,
  "data": {
    "id": "job_xxx",
    "status": "completed",
    "completed": 50,
    "total": 50,
    "data": [
      {
        "url": "https://example.com/page1",
        "markdown": "...",
        "meta": {"statusCode": 200, "title": "...", ...}
      }
    ]
  },
  "meta": {
    "creditsRemaining": 998,
    ...
  }
}
```

**Progress detection**: use `data.status`. Values observed: `"queued"`, `"running"`, `"completed"`, `"failed"`. Fall back to `data.completed == data.total` when the field isn't present.

**Warmup window**: for ~5–10 seconds after `POST /crawl` returns a `job_id`, the very first poll can return `success:false` with `error.code: "NOT_FOUND"`. This is the job still registering, not a real failure. **Tolerate it**: sleep 5s and retry up to 3 times before treating the job as truly missing. `NOT_FOUND` returns are not charged.

**TTL on completed jobs**: completed jobs are purged from the lookup index after a short retention window (observed: within seconds-to-minutes after completion). Plan to read all results in your first successful poll after `status == "completed"`. If you need long-term storage of the result set, persist it yourself.

**Cross-tenant 404**: polling a job_id that belongs to a different API key returns the same `NOT_FOUND` shape — indistinguishable from "job not found" or "expired" by design.

### ⚠️ Cloudflare User-Agent block (HTTP clients other than curl)

The Cloudflare edge in front of `api.zoodata.ai` rejects requests with the default `Python-urllib/X.Y` User-Agent (and likely some other "scripted" defaults), returning **HTTP 403 with Cloudflare error code 1010** (HTML body, not the API envelope). Verified:

| Client / UA | Result |
|---|---|
| `curl/8.x` (default) | ✅ 200 |
| `Python-urllib/3.10` (default) | ❌ 403 (Cloudflare 1010) |
| `Python-urllib/3.10` + custom `User-Agent: web-extract-skill/1.0` | ✅ 200 |

**Rule**: any HTTP client other than curl must set an explicit `User-Agent`. Any non-default string is accepted. This applies to ALL endpoints (`/scrape`, `/search`, `/map`, `/crawl`, `/crawl/{id}`), not just crawl-status — the block is at the edge, before routing.

---

## Versioning

WebTools currently exists **only under `/openapi/v2/webtools/*`**. There's no v3 variant. The `/openapi/v3/*` prefix is reserved for endpoints with breaking protocol changes (currently only `/realtime/product`). If/when webtools gains a v3, this skill will be updated.

## Rate limits

Per-API-key limits (set by subscription tier):

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit-RPM` | Requests/min allowed |
| `X-RateLimit-Remaining-RPM` | Remaining in current window |
| `X-RateLimit-Reset` | Unix timestamp when window resets |
| `X-RateLimit-Limit-Concurrency` | Max concurrent requests |
| `Retry-After` (on 429 only) | Seconds to wait |

On 429, the API returns a `Retry-After` header (seconds). Honor it: wait that long, then retry once; if it fails again, back off exponentially (2x, 4x). Long crawls + tight polling intervals can hit concurrency caps — space polls ≥5s apart and fetch with `limit=1000` per poll to minimize call count.

## Cross-endpoint quirks worth remembering

| Concern | Detail |
|---|---|
| `scrape` raw HTML field name | `data.rawHtml` (not `data.html`) |
| `crawl` default `limit` | 100 (conservative — caller can raise up to 10000) |
| `crawl` vs `map` `ignoreQueryParameters` default | `crawl` defaults `false`, `map` defaults `true` — opposite |
| `search` returned result count | May be less than `limit` when deep-scrape mode drops empty pages |
| `crawl-status` `data` shape | An **array** of page-scrape blobs (not the object envelope you see elsewhere) |
| `crawl-status` 404 | Could mean unknown id OR cross-tenant job — indistinguishable by design |

## Credits dashboard

`meta.creditsRemaining` is returned on every successful call. For a cheap fresh snapshot, scrape `https://example.com` (1 credit, ~1s) and read `meta.creditsRemaining` from the response.
