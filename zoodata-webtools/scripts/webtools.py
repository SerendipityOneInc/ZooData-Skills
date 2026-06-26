#!/usr/bin/env python3
"""
ZooData WebTools CLI — scrape, crawl, map, search the open web

8 subcommands wrapping 6 endpoints under /openapi/v2/webtools/* with the
quirks baked in:
  - Custom User-Agent (Cloudflare blocks the default Python-urllib UA)
  - Default formats=["json"] (skill convention — no LLM-side extract cost)
  - crawl-status warmup tolerance (NOT_FOUND for ~10s after submit is normal)
  - crawl-status nested data shape (pages live at data.data, not data)

Usage:
    webtools.py scrape <url> [--format json|markdown|rawHtml ...]
    webtools.py interactive <url> --actions '<json>' [--format ...]
    webtools.py search <query> [--limit N] [--sources ...] [--tbs ...]
                               [--include-domains ...] [--exclude-domains ...]
                               [--scrape-format json|markdown]
    webtools.py map <url> [--limit N] [--search kw] [--sitemap-mode ...]
                          [--include-paths ...] [--exclude-paths ...]
                          [--no-subdomains] [--keep-query-params]
    webtools.py crawl <url> [--limit N] [--max-depth N] [--include-paths ...]
                            [--exclude-paths ...] [--allow-subdomains]
                            [--sitemap-mode ...] [--ignore-query-params]
                            [--crawl-entire-domain]
    webtools.py crawl-status <job-id> [--skip N] [--limit N]
    webtools.py crawl-wait <url> [<crawl args>] [--poll-interval 5]
                                 [--max-wait 1800]
    webtools.py check

Auth:
    ZOODATA_API_KEY env (legacy: APICLAW_API_KEY). Falls back to
    ~/.zoodata/config.json or ~/.apiclaw/config.json (key: api_key).
    Get a free key at https://zoodata.ai/en/api-keys.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "https://api.zoodata.ai/openapi/v2/webtools"
USER_AGENT = "zoodata-webtools-skill/1.0 (python)"
DEFAULT_TIMEOUT = 200       # scrape SLA 120s, interactive 180s — leave buffer
MAX_RETRIES = 3
RETRY_DELAY = 2
MIN_REQUEST_INTERVAL = 0.6  # ≤100 req/min default RPM cap
DEFAULT_FORMATS = ["json"]  # skill convention: JSON-first

_last_request_time = 0.0


# ─── Auth ────────────────────────────────────────────────────────────────────

def get_api_key():
    key = (
        os.environ.get("ZOODATA_API_KEY", "").strip()
        or os.environ.get("APICLAW_API_KEY", "").strip()
    )
    if key:
        return key
    for path in ("~/.zoodata/config.json", "~/.apiclaw/config.json"):
        p = os.path.expanduser(path)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    k = json.load(f).get("api_key", "").strip()
                    if k:
                        return k
            except (json.JSONDecodeError, IOError):
                pass
    print("ERROR: ZOODATA_API_KEY not set. Get one at "
          "https://zoodata.ai/en/api-keys", file=sys.stderr)
    sys.exit(2)


# ─── HTTP ────────────────────────────────────────────────────────────────────

def _headers():
    # User-Agent is REQUIRED — Cloudflare edge returns 403 (error code 1010)
    # for the default Python-urllib UA.
    return {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }


def request(method, path, body=None, query=None, timeout=DEFAULT_TIMEOUT):
    """Call /webtools. Returns parsed JSON or a synthesized error envelope."""
    global _last_request_time

    url = f"{BASE_URL}/{path.lstrip('/')}"
    if query:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in query.items() if v is not None})

    data = json.dumps(body).encode("utf-8") if body is not None else None

    # Simple pacing: keep ≥0.6s between requests
    elapsed = time.monotonic() - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    delay = RETRY_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        _last_request_time = time.monotonic()
        try:
            req = urllib.request.Request(url, data=data, headers=_headers(),
                                         method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            status = e.code
            body_text = e.read().decode("utf-8", errors="replace") if e.fp else ""
            try:
                err_json = json.loads(body_text)
            except json.JSONDecodeError:
                err_json = {"raw": body_text[:500]}
            if status == 401:
                print("API key invalid or expired. Get a new one at "
                      "https://zoodata.ai/en/api-keys", file=sys.stderr)
                sys.exit(3)
            if status == 402:
                print("Credit exhausted. Top up at "
                      "https://zoodata.ai/en/pricing", file=sys.stderr)
                print(json.dumps(err_json, indent=2), file=sys.stderr)
                sys.exit(4)
            if status == 429 and attempt < MAX_RETRIES:
                retry_after = float(e.headers.get("Retry-After", delay))
                time.sleep(retry_after)
                delay *= 2
                continue
            if 500 <= status < 600 and attempt < MAX_RETRIES:
                time.sleep(delay)
                delay *= 2
                continue
            return {
                "success": False,
                "error": {"code": f"HTTP_{status}", "message": e.reason,
                          "details": err_json},
                "meta": {"requestPath": path},
            }
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < MAX_RETRIES:
                time.sleep(delay)
                delay *= 2
                continue
            return {
                "success": False,
                "error": {"code": "NETWORK", "message": str(e)},
                "meta": {"requestPath": path},
            }
    return {"success": False, "error": {"code": "RETRY_EXHAUSTED"}}


def output(obj):
    if sys.stdout.isatty():
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(obj, ensure_ascii=False))


def _csv(s):
    if not s:
        return None
    return [item.strip() for item in s.split(",") if item.strip()]


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_scrape(args):
    body = {"url": args.url, "formats": args.format or DEFAULT_FORMATS}
    output(request("POST", "scrape", body=body))


def cmd_interactive(args):
    try:
        actions = json.loads(args.actions)
    except json.JSONDecodeError as e:
        print(f"--actions must be a JSON array: {e}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(actions, list):
        print("--actions must be a JSON array", file=sys.stderr)
        sys.exit(2)
    body = {
        "url": args.url,
        "actions": actions,
        "formats": args.format or DEFAULT_FORMATS,
    }
    output(request("POST", "scrape-interactive", body=body))


def cmd_search(args):
    body = {"query": args.query, "limit": args.limit}
    if args.sources:
        body["sources"] = _csv(args.sources)
    if args.tbs:
        body["tbs"] = args.tbs
    if args.include_domains:
        body["includeDomains"] = _csv(args.include_domains)
    if args.exclude_domains:
        body["excludeDomains"] = _csv(args.exclude_domains)
    # Skill convention: when user opts into deep-scrape, default to JSON.
    if args.deep_scrape and not args.scrape_format:
        body["scrapeOptions"] = {"format": "json"}
    elif args.scrape_format:
        body["scrapeOptions"] = {"format": args.scrape_format}
    output(request("POST", "search", body=body))


def cmd_map(args):
    body = {
        "url": args.url,
        "limit": args.limit,
        "sitemapMode": args.sitemap_mode,
        "includeSubdomains": not args.no_subdomains,
        "ignoreQueryParameters": not args.keep_query_params,
    }
    if args.search:
        body["search"] = args.search
    if args.include_paths:
        body["includePaths"] = _csv(args.include_paths)
    if args.exclude_paths:
        body["excludePaths"] = _csv(args.exclude_paths)
    output(request("POST", "map", body=body))


def _build_crawl_body(args):
    body = {
        "url": args.url,
        "limit": args.limit,
        "allowSubdomains": args.allow_subdomains,
        "sitemapMode": args.sitemap_mode,
        "ignoreQueryParameters": args.ignore_query_params,
        "crawlEntireDomain": args.crawl_entire_domain,
    }
    if args.max_depth is not None:
        body["maxDepth"] = args.max_depth
    if args.include_paths:
        body["includePaths"] = _csv(args.include_paths)
    if args.exclude_paths:
        body["excludePaths"] = _csv(args.exclude_paths)
    return body


def cmd_crawl(args):
    output(request("POST", "crawl", body=_build_crawl_body(args)))


def cmd_crawl_status(args):
    query = {}
    if args.skip is not None:
        query["skip"] = args.skip
    if args.limit is not None:
        query["limit"] = args.limit
    output(request("GET", f"crawl/{args.job_id}", query=query or None))


def cmd_crawl_wait(args):
    """Submit a crawl, tolerate the warmup NOT_FOUND window, poll until done."""
    submit = request("POST", "crawl", body=_build_crawl_body(args))
    if not submit.get("success"):
        output(submit)
        sys.exit(1)
    job_id = submit["data"]["id"]
    print(f"crawl submitted: job_id={job_id}", file=sys.stderr)

    deadline = time.monotonic() + args.max_wait
    pages, last_total, stable, warmup_misses = [], -1, 0, 0
    while time.monotonic() < deadline:
        status = request("GET", f"crawl/{job_id}",
                         query={"skip": len(pages), "limit": 100})
        if not status.get("success"):
            code = status.get("error", {}).get("code")
            # Warmup window: first ~10s after submit may return NOT_FOUND.
            # Tolerate up to 3 such polls before giving up.
            if code == "NOT_FOUND" and warmup_misses < 3:
                warmup_misses += 1
                print(f"  warmup poll: NOT_FOUND ({warmup_misses}/3)",
                      file=sys.stderr)
                time.sleep(args.poll_interval)
                continue
            output(status)
            sys.exit(1)
        d = status["data"]
        # ⚠️ NOT data.length — pages live at data.data
        pages.extend(d.get("data", []) or [])
        total = d.get("total", len(pages))
        st = d.get("status", "?")
        print(f"  status={st} {len(pages)}/{total} pages "
              f"(credits={status.get('meta', {}).get('creditsRemaining')})",
              file=sys.stderr)
        if st == "completed":
            break
        if total == last_total:
            stable += 1
        else:
            stable, last_total = 0, total
        if total > 0 and len(pages) >= total and stable >= 2:
            break
        time.sleep(args.poll_interval)

    final_total = last_total if last_total >= 0 else len(pages)
    output({
        "success": True,
        "data": {"id": job_id, "status": "completed",
                 "completed": len(pages), "total": final_total,
                 "data": pages},
        "meta": {"polled": True},
    })


def cmd_check(_args):
    print(f"ZooData WebTools — health check against {BASE_URL}\n",
          file=sys.stderr)
    probe = request("POST", "scrape",
                    body={"url": "https://example.com",
                          "formats": DEFAULT_FORMATS})
    ok = probe.get("success")
    print(f"  /scrape          {'OK' if ok else 'FAIL'}", file=sys.stderr)
    meta = probe.get("meta", {})
    if "creditsRemaining" in meta:
        print(f"  credits left:    {meta['creditsRemaining']}",
              file=sys.stderr)
    if not ok:
        print(json.dumps(probe.get("error"), indent=2), file=sys.stderr)
        sys.exit(1)
    output({"check": "ok", "creditsRemaining": meta.get("creditsRemaining")})


# ─── CLI ─────────────────────────────────────────────────────────────────────

def _crawl_args(s):
    s.add_argument("url")
    s.add_argument("--limit", type=int, default=100)
    s.add_argument("--max-depth", type=int)
    s.add_argument("--include-paths", help="Comma-separated regex patterns")
    s.add_argument("--exclude-paths", help="Comma-separated regex patterns")
    s.add_argument("--allow-subdomains", action="store_true")
    s.add_argument("--sitemap-mode", default="include",
                   choices=["include", "only", "skip"])
    s.add_argument("--ignore-query-params", action="store_true")
    s.add_argument("--crawl-entire-domain", action="store_true")


def build_parser():
    p = argparse.ArgumentParser(
        prog="webtools.py",
        description="ZooData WebTools CLI — JSON-first, no extraction needed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("scrape", help="Scrape a single URL (default: JSON)")
    s.add_argument("url")
    s.add_argument("--format", action="append",
                   choices=["json", "markdown", "rawHtml"],
                   help="Repeatable; default json (skill convention)")
    s.set_defaults(func=cmd_scrape)

    s = sub.add_parser("interactive",
                       help="Scrape after browser actions (default: JSON)")
    s.add_argument("url")
    s.add_argument("--actions", required=True,
                   help='JSON array, e.g. [{"type":"wait","milliseconds":2000}]')
    s.add_argument("--format", action="append",
                   choices=["json", "markdown", "rawHtml"])
    s.set_defaults(func=cmd_interactive)

    s = sub.add_parser("search", help="Web search (SERP-only or deep-scrape)")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--sources", help="Comma-separated: web,news,images")
    s.add_argument("--tbs", help="Time filter: qdr:d|qdr:w|qdr:m|qdr:y")
    s.add_argument("--include-domains", help="Comma-separated bare hostnames")
    s.add_argument("--exclude-domains", help="Comma-separated bare hostnames")
    s.add_argument("--scrape-format", choices=["json", "markdown"],
                   help="Deep-scrape format (default json when --deep-scrape)")
    s.add_argument("--deep-scrape", action="store_true",
                   help="Enable deep-scrape (json by default)")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("map", help="Discover URLs reachable from a seed URL")
    s.add_argument("url")
    s.add_argument("--limit", type=int, default=5000)
    s.add_argument("--search", help="Keyword filter for discovered URLs")
    s.add_argument("--sitemap-mode", default="include",
                   choices=["include", "only", "skip"])
    s.add_argument("--no-subdomains", action="store_true",
                   help="Exclude subdomains of the seed host")
    s.add_argument("--include-paths", help="Comma-separated regex patterns")
    s.add_argument("--exclude-paths", help="Comma-separated regex patterns")
    s.add_argument("--keep-query-params", action="store_true",
                   help="Treat ?a=1 and ?a=2 as distinct URLs")
    s.set_defaults(func=cmd_map)

    s = sub.add_parser("crawl", help="Submit an async recursive crawl job")
    _crawl_args(s)
    s.set_defaults(func=cmd_crawl)

    s = sub.add_parser("crawl-status", help="Poll a crawl job by id")
    s.add_argument("job_id")
    s.add_argument("--skip", type=int)
    s.add_argument("--limit", type=int)
    s.set_defaults(func=cmd_crawl_status)

    s = sub.add_parser("crawl-wait",
                       help="Submit a crawl AND block until it completes "
                       "(tolerates warmup NOT_FOUND)")
    _crawl_args(s)
    s.add_argument("--poll-interval", type=int, default=5,
                   help="Seconds between polls (default 5)")
    s.add_argument("--max-wait", type=int, default=1800,
                   help="Max seconds to wait (default 1800)")
    s.set_defaults(func=cmd_crawl_wait)

    s = sub.add_parser("check", help="Verify auth + connectivity (1 credit)")
    s.set_defaults(func=cmd_check)

    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
