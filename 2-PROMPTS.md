# Prompts for Claude Code on the day

Your starter repo's `CLAUDE.md` already carries the rules (the spec is the source of truth, never edit a test to pass, the test layers, domain traps), so the prompts can stay short. **Read the spec yourself before prompt 1.**

Tip: save this file somewhere you can open on the Ohme laptop: it's in your starter repo.

---

## 🚨 Emergency: start from nothing (one prompt, about 30 minutes to the first test)

Use this if you can't clone the repo, or you've forgotten everything. Fill in the 3 blanks.

```
I have 30 minutes. Spec: <SPEC FILE>. API: <URL>. Token: <TOKEN or "none">.
Do these steps in order, briefly:
1. Build a minimal Python pytest API test framework in this folder:
   - requirements.txt: pytest, requests, jsonschema, pytest-html
   - framework/api_client.py: base URL and bearer token from env vars BASE_URL and API_TOKEN; per-call auth option (no header, or a wrong token)
   - framework/assertions.py: assert_status(resp, code) and explain(resp) that prints the body and a curl command to reproduce
   - conftest.py: an `api` fixture and a `valid_body` fixture (a valid request body; tests override one field)
   - pytest.ini with markers: smoke, contract, negative, boundary, security, integration
   - .github/workflows/api-tests.yml: on every pull request, install, run smoke tests first, then the full suite, upload reports
   - CLAUDE.md with rules: the spec is the source of truth; assert what the spec says, never what the API returns; never edit a test to make it pass; test min, max, min-1, max+1 and the equal case; watch kW vs kWh, pence vs pounds, UTC with Z
   - FINDINGS.md with sections: product bugs, spec questions, test limitations
2. Install the requirements and set BASE_URL and API_TOKEN for this session.
3. Read the spec. Give me a short test plan: about 15 rows per endpoint, P1 first, top 5 spec questions. Only inputs we can send. No code yet.
4. Write ONE happy-path test for the first endpoint and run it. Show me the result.
Then stop and wait for me.
```

**Short version (if you can't copy anything):**
"Build a pytest API test framework here from scratch: client with auth, curl repro on failure, env config, markers, GitHub Actions, CLAUDE.md rules, FINDINGS.md. Then read <spec>, give me a short test plan, write one test and run it. API <URL>, token <token>."

After that, carry on with the short versions below: "now write P1 tests for <endpoint>…".

---

## Short versions (easy to remember: Plan → Write → Review → Run → Report)

| Step | Type this |
|---|---|
| 1. Plan | `Read <spec>. Make a test plan table, about 15 rows per endpoint, P1 first, top 5 spec questions. No code yet.` |
| 2. Write | `Fix: <what's wrong>. Then write P1 tests for <endpoint>, about 10, use parametrize.` |
| 3. Review | `Review your tests. Which could pass even if the API is wrong?` |
| 4. Run | `Run the tests. Sort failures into product bug, test bug or spec question. Don't change tests to pass.` |
| 5. Report | `Fill FINDINGS.md from the results, most serious bug first.` |

Shortcut: `Read 2-PROMPTS.md and do prompt 1 using <spec file>. The API is at <URL>, token <token>.` Then "now do prompt 2", and so on.

---

### 0. Build the skeleton from scratch (if you can't use this repo)
```
Create a minimal Python API test framework in this folder:
- requirements.txt: pytest, requests, jsonschema, pytest-html
- framework/api_client.py: ApiClient with base URL, optional bearer token,
  and an auth argument per call (auth=False for no header)
- framework/assertions.py: assert_status(resp, code) and explain(resp) that
  print the response body and a curl command to reproduce it
- conftest.py: an `api` fixture using env vars BASE_URL and API_TOKEN, and a
  `valid_body` fixture that returns a valid request body with one field overridden
- pytest.ini with markers: smoke, contract, negative, boundary, security, integration
- tests/test_smoke.py: checks the API is reachable
- .github/workflows/api-tests.yml: on every pull request, install, run smoke
  tests first, then the full suite, and upload the reports
- FINDINGS.md with sections: product bugs, spec questions, test limitations
- SPEC_NOTES.md with, per endpoint: who can call it, what can I send, what can go
  wrong, what comes back, what must always be true; plus a "what's unclear" section
Rule: tests must assert what the spec says, never what the API returns.
Then run the smoke test.
```

**Short version (if you have nothing to copy from):**
"Create a pytest API test framework: an API client with auth, failures that show a curl repro, config from environment variables, a valid-body fixture, test markers, a GitHub Actions CI file, a FINDINGS.md and a SPEC_NOTES.md."

### 1. Spec → test matrix (about minute 3, no code yet)
```
Read <SPEC file>. Act as a senior QA engineer. Produce a table of test cases per endpoint:
priority (P1-P3 by customer impact) | layer (contract, business rule, boundary, negative,
missing field, auth, cross-endpoint, data sanity) | input | expected status + error code |
the spec line it comes from.
Keep it short: about 15 rows per endpoint, P1 first. Only test inputs we can send;
check response fields in the reply.
Only expected results the spec states. Anything the spec doesn't say goes in a separate
"Spec questions" list (top 5 only). Include min, min-1, max, max+1 and the equal case for
every > or < rule. Include at least one test where the two endpoints must agree. No code yet.
```

### 2. Matrix → pytest (one endpoint at a time)
```
Write pytest tests for the P1 rows for <METHOD /path> (about 10 test functions) in tests/test_<name>.py,
following CLAUDE.md and tests/endpoint_template.py. Fill VALID_BODY in conftest.py from the
spec. Use parametrize for boundaries and invalid values, schema checks for the contract, and
one rule per test. Don't assert anything the spec doesn't state. Don't run them yet.
```

### 3. Review before running (say what you find out loud)
```
Review the tests you just wrote. Which could pass even if the API were wrong? List weak
assertions, any expected value not taken from the spec, any > vs >= mistakes, unit or
timezone mistakes, and spec rules not yet covered. Don't change files yet.
```

### 4. Triage
```
Run pytest -rA. For each failure decide: product bug, test bug, or spec ambiguity, and quote
the spec line. Group failures by root cause. Suggest severity for an EV home-charging customer.
Do not change any test to match the API.
```

### 5. Write up
```
Fill FINDINGS.md from the triage: headline line first, then product bugs as
"spec says / API does / impact / test", ordered by severity, then spec questions and test
limitations.
```

### Prose spec (Markdown or PDF)
```
The spec is prose. Turn each response and error it describes into a JSON Schema dict at the
top of the test file (required fields, types, enums, min/max, formats). List any rule that
can't be expressed in a schema; we'll test those separately.
```

---

## What to check in AI output (say these out loud: this is what Andy is watching for)
- **Invented rules:** asserts behaviour the spec never states. Delete it or move it to spec questions.
- **Asserting current behaviour:** if expected values came from calling the API, the bugs are baked in.
- **Wrong boundaries:** `>` vs `>=` is the most common mistake. Check every one.
- **Units:** kW vs kWh, pence vs pounds, seconds vs milliseconds.
- **Time:** naive datetimes, local vs UTC, tests that only pass at certain times of day.
- **Weak assertions:** `assert r.ok` where the spec says exactly `201`.

**Change or reject at least one thing out loud.** It proves you're in charge, and it's your honest example for the AI workflow question.
