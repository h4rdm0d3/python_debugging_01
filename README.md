# python_debugging_01

A Python web crawler service with several bugs. Your job is to make it correctly handle the workload the validator throws at it, within the resource envelope the platform provisions.

This is the first course on the [hardmode](https://github.com/h4rdm0d3) platform. The service ships as an HTTP server. A private validator hits it, scores your fixes, and shows you a red → amber → green progression.

## The contract

The service exposes:

### `POST /crawl`

Request:
```json
{ "urls": ["https://example.com/a", "https://example.com/b"], "mode": "batch" }
```

`mode` is optional.

- `"batch"` (the default) — fetches concurrently and returns once every fetch resolves.
- `"stream"` — fetches concurrently and returns as soon as the work is dispatched.

Both modes should produce the same eventual result set for the same input.

Response:
```json
{
  "results": [
    { "url": "https://example.com/a", "title": "A", "error": null },
    { "url": "https://example.com/b", "title": "B", "error": null }
  ],
  "stats": { "instance_seen": ["https://example.com/a", "https://example.com/b"] }
}
```

`stats.instance_seen` reports the URLs handled by the crawler instance that served the request.

### `GET /healthz`

Returns `{"ok": true}`. Used by the grader to know the service is up.

## How you're graded

The validator runs a battery of tasks against your service. Each task:

- Sends a specific workload.
- Knows the correct response by computing it from ground truth ahead of time.
- Has a performance bar — latency, throughput, sometimes memory.
- Passes when your service matches both the response and the bar.

Score is the sum of weights of passing tasks, in `[0, 100]`. Label:

- **red** — `score < 25`
- **amber** — `25 ≤ score < 100`
- **green** — `score == 100`

You see `{score, label}` only. No per-task breakdown. The validator deliberately does not point at bugs — it tells you whether your service met the bar, not what shape your fix should take.

## Resource envelope

The platform runs your service with:

- CPU: 200m
- Memory: 256Mi
- Network: egress restricted to the platform's fixture (no internet at grade time)

The performance bars are calibrated so an approximately-correct service can't clear them within these caps. Performance is part of correctness here. (Local development runs without caps, so the bar is harder to feel locally — beat the workload first, then think about whether your fix would survive a 256Mi container.)

## Running locally

The repo ships a `compose.yaml` that brings up your crawler alongside the same Wikipedia-shaped fixture the platform's grader uses (`ghcr.io/ltbringer/python_debugging_01-fixture`). The crawler runs under the same CPU and memory caps the platform enforces at grade time.

```bash
docker compose up --build
```

Then in another shell, POST to the crawler with URLs pointing at the fixture's compose-network hostname:

```bash
curl -sX POST localhost:8080/crawl \
  -H 'content-type: application/json' \
  -d '{"urls":[
    "http://fixture:9090/wiki/Python_(programming_language)",
    "http://fixture:9090/wiki/Asyncio",
    "http://fixture:9090/wiki/Global_interpreter_lock"
  ]}' | jq
```

`GET http://localhost:9090/catalog` lists the slugs the fixture knows about. `GET /wiki/<slug>` accepts a few query-string overlays for testing specific behaviors — see the fixture's README.

The bugs in this codebase manifest more visibly under the compose's CPU/memory caps than they do in an unconstrained `uv run` loop. If you want a faster iteration cycle, comment out `mem_limit` and `cpus` in `compose.yaml`. Restore them before deciding your service is "done" — the validator's performance bars are calibrated for the constrained envelope.

### Without Docker

```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
```

The service listens on `:8080`. The crawler is generic — it makes HTTP GETs and treats responses as JSON, so URLs can point at anything that returns JSON (the fixture above, the live Wikipedia REST API, your own mock).

The happy path works. The defects only manifest under specific conditions. Debug from outcomes: send workloads, compute what the response should be, compare to what came back.

## Forking and submitting

1. Fork this repo.
2. Fix the service.
3. Commit, push, and tag a new semver (`git tag v1.0.1 && git push --tags`). GitHub Actions builds and pushes `ghcr.io/<you>/python_debugging_01:v1.0.1` (public) to GHCR.
4. From the hardmode CLI:
   ```bash
   hardmode session submit
   ```
5. Watch the score climb through red → amber → green.

The validator's fixture is deterministic. A passing run on your machine will pass on the platform. There is no flakiness budget.

Good luck.
