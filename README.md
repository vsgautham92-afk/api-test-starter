# API test starter (Python)

A small, ready-to-run framework for testing an HTTP API against a spec: pytest + requests + jsonschema. Failures print a curl repro, reports come out as HTML and JUnit, and a GitHub Actions workflow runs it on every change.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

BASE_URL=http://localhost:8000 API_TOKEN=xyz pytest -q
# Windows PowerShell: $env:BASE_URL="http://localhost:8000"; $env:API_TOKEN="xyz"; pytest -q
```

Config comes from environment variables: `BASE_URL`, `API_TOKEN`, and optionally `SPEC_PATH` (an OpenAPI file for schema checks by name).

## Structure

```
framework/api_client.py   base URL, auth per call, timeouts, connection retries
framework/assertions.py   assert_status / explain: response + curl repro on every failure
framework/schema.py       validate against OpenAPI component schemas or inline schemas
conftest.py               fixtures: api, spec, valid_body (one-field overrides)
tests/test_smoke.py       proves the service is reachable
tests/endpoint_template.py   the layered pattern to copy per endpoint
.github/workflows/api-tests.yml   smoke gate, then full suite, on every push and PR
CLAUDE.md                 conventions for AI-assisted test writing
FINDINGS.md               product bugs, spec questions, test limitations
SPEC_NOTES.md             fill in during the first 3 minutes, before any code
```

## Design choices
- **The spec is the oracle.** A failing test is a mismatch to investigate, never a test to "fix".
- **Valid-body factory.** Each test overrides one field of a known-good body, so every failure has one cause.
- **Table-driven boundaries.** Adding a case is one line.
- **Failures are bug reports.** Each one shows the response and a curl command to reproduce it.
- **Fail fast in CI.** Smoke on every PR, then the full suite; known ticketed bugs use `xfail(strict=True)`, so the pipeline stays green without hiding them.
- **Env-driven config.** The same suite runs locally, in CI and against staging.
