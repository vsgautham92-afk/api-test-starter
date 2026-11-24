# Prompts for Claude Code on the day

Your starter repo's `CLAUDE.md` already carries the rules (the spec is the source of truth, never edit a test to pass, the test layers, domain traps), so the prompts can stay short. **Read the spec yourself before prompt 1.**

Tip: save this file somewhere you can open on the Ohme laptop: it's in your starter repo.

---

### 1. Spec → test matrix (about minute 3, no code yet)
```
Read <SPEC file>. Act as a senior QA engineer. Produce a table of test cases per endpoint:
priority (P1-P3 by customer impact) | layer (contract, business rule, boundary, negative,
missing field, auth, cross-endpoint, data sanity) | input | expected status + error code |
the spec line it comes from.
Only expected results the spec states. Anything the spec doesn't say goes in a separate
"Spec questions" list. Include min, min-1, max, max+1 and the equal case for every > or <
rule. Include at least one test where the two endpoints must agree. No code yet.
```

### 2. Matrix → pytest (one endpoint at a time)
```
Write pytest tests for the P1 and P2 rows for <METHOD /path> in tests/test_<name>.py,
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
