# Project instructions for Claude Code

This repo is an API test framework (Python, pytest, requests, jsonschema). It tests an HTTP API against a written spec. The goal is to find where the API does not match the spec, not to make tests pass.

## Layout
- `framework/api_client.py`: `ApiClient`. Use the `api` fixture; never call `requests` directly. Auth per call: `auth=False` (no header) or `auth="Bearer wrong"`.
- `framework/assertions.py`: `assert_status(resp, code)`, `json_body(resp)`, `explain(resp)`. Failures print the response and a **curl repro**. Put `explain(r)` in any bare `assert`.
- `framework/schema.py`: `assert_matches_schema(body, "SchemaName", spec)` for OpenAPI component schemas, or pass an inline JSON Schema dict when the spec is prose.
- `conftest.py`: fixtures `api`, `base_url`, `spec`, and `valid_body` (fill `VALID_BODY` from the spec; tests override one field each).
- `tests/endpoint_template.py`: the pattern to copy per endpoint.
- `FINDINGS.md`: product bugs, spec questions, test limitations.

## Rules for writing tests
1. **The spec is the source of truth.** Assert what the spec states, never what the API currently returns. If the API disagrees, the test must fail. **Never edit a test to make it pass.**
2. **Don't invent rules.** If the spec doesn't state an expected result, don't assert one; list it under "Spec questions" in `FINDINGS.md` instead.
3. One file per endpoint (`tests/test_<endpoint>.py`), plus `tests/test_cross_endpoint.py` for behaviour spanning both. Test names read like requirements.
4. Work through the layers in order: contract (exact status code, Content-Type, schema, error body shape, required headers); business rules (recalculate derived values like totals and costs yourself, using `pytest.approx` for floats); boundaries (min and max accepted, min-1 and max+1 rejected, and the **equal** case for every `>` or `<` rule); types and missing fields (wrong type, `null`, each required field missing, broken JSON; any 500 is a finding); auth on **each** endpoint (missing, wrong, no `Bearer` prefix); across endpoints (write with one, read with the other); data sanity (fields that must agree, e.g. status vs power); quick non-functional (unknown route, wrong method).
5. Use `@pytest.mark.parametrize` for boundaries and invalid values; one rule per test; start POST bodies from `valid_body()` and override one field.
6. Markers: `smoke`, `contract`, `negative`, `boundary`, `security`, `integration`.
7. Watch for domain traps: kW vs kWh, pence vs pounds, UTC vs Europe/London, a `Z` suffix on timestamps, `>` vs `>=`, half-hour alignment. Generate times relative to now; never hard-code dates that go stale.
8. Weak assertions are not allowed: no `assert r.ok` where the spec says an exact status, no status-only checks when a body is specified.

## When tests fail
Classify each failure as a **product bug** (quote the spec line), a **test bug** (fix the test), or a **spec ambiguity** (move it to Spec questions and delete or skip the test). Group failures by root cause. Only mark a test `xfail(strict=True, reason=...)` if asked to.

## Running
```
pytest -q                  # everything
pytest -m smoke            # fast subset
pytest -x --lf             # rerun only the last failures
pytest -rA                 # summary of every result (paste into triage)
```
