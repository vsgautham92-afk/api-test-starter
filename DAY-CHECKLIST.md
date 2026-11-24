# Day checklist: coding task (Wed 2 Dec, 12:30–13:15, with Andy)

Repo: https://github.com/vsgautham92-afk/api-test-starter
Prompts: https://github.com/vsgautham92-afk/api-test-starter/blob/main/2-PROMPTS.md

---

## Before the clock starts (about 2–5 min)
- [ ] Ask: **"Shall I talk as I go, or walk you through at the end?"**
- [ ] Ask: **"Is it OK to start from a small template I use, or would you prefer I build the framework from scratch?"**
- [ ] Ask: **"What's the base URL for the API?"** (and whether it needs a token)
- [ ] Open VS Code → **Terminal → New Terminal** (or Ctrl + `)

### Route A: template allowed
- [ ] `git clone https://github.com/vsgautham92-afk/api-test-starter.git`
      (backup: open the repo in the browser → **Code → Download ZIP** → unzip)
- [ ] **File → Open Folder** → `api-test-starter` → **Yes, I trust**
- [ ] `python -m pip install -r requirements.txt`
- [ ] `$env:BASE_URL="<address from Andy>"; python -m pytest -m smoke` → **1 passed**

### Route B: build from scratch
- [ ] Create an empty folder (e.g. `ohme-api-tests`) → **File → Open Folder** → select it
- [ ] Open `2-PROMPTS.md` on GitHub in the browser → copy **prompt 0**
      (no browser? say the short version: client with auth, curl repro on failure,
      env config, valid-body fixture, markers, GitHub Actions CI, FINDINGS.md)
- [ ] Paste it into Claude Code
- [ ] **While it builds: read the spec and fill in your notes** (next section). No time wasted.
- [ ] **Check what it built, out loud:**
  - [ ] `requirements.txt` has pytest, requests, jsonschema
  - [ ] the API client reads `BASE_URL` and the token from environment variables
  - [ ] failures print the response and a curl command
  - [ ] `pytest.ini` has markers (smoke, negative, boundary…)
  - [ ] `.github/workflows/api-tests.yml` runs on every pull request
  - [ ] `FINDINGS.md` exists
- [ ] Ask Claude Code to add a short `CLAUDE.md`: "Tests must assert the spec, never what the
      API returns; never change a test to make it pass; don't invent rules."
- [ ] `python -m pip install -r requirements.txt`
- [ ] `$env:BASE_URL="<address from Andy>"; python -m pytest -m smoke` → **1 passed**
- [ ] Say: *"I've built a lot of these, so I know what the skeleton needs. I let AI do the
      typing and checked it against that list."*

---

## Minutes 0–3: READ (no code)
- [ ] Read the spec yourself; save it into the folder if it's a file
- [ ] Fill in **SPEC_NOTES.md** (Route B: make a notes file), 5 questions per endpoint:
  1. **Who can call it?** (auth: missing or wrong token?)
  2. **What can I send?** (limits, allowed values, formats; edge values to try)
  3. **What can go wrong?** (every status code)
  4. **What comes back?** (fields, types, formats)
  5. **What must always be true?** (rules in words, links between the endpoints)
  - plus **What's unclear?**
- [ ] Say: *"Before any code, I'm listing the rules I'll test against."*

## Minutes 3–4: LOOK
- [ ] Claude Code: **"Curl both endpoints once with valid requests and show me the responses."**
- [ ] The spec is still the truth.

## Minutes 4–6: PLAN
- [ ] Paste **prompt 1** (test plan)
- [ ] Compare with your notes out loud: *"It missed X, I'll add it."*

## Minutes 6–20: BUILD
- [ ] **Prompt 2** for endpoint 1 → **check every test out loud**:
  - status-only checks (no body check)
  - expected values the spec never states (AI guessed)
  - wrong status code (e.g. 404 where the spec says 400)
  - `>` vs `>=`, kW vs kWh, timezones, missing `Z`
- [ ] Change or reject **at least one thing** out loud
- [ ] `python -m pytest -q`
- [ ] Repeat for endpoint 2
- [ ] Add one test where **both endpoints must agree**
- [ ] Run the suite **every 5 minutes**
- [ ] If a test fights you for 2 minutes → skip it, say why, move on

## Minutes 20–24: TRIAGE
- [ ] Each red test: **"Their API or my test?"** → check the spec
- [ ] Sort: **product bug** / **spec question** / **test limitation**
- [ ] FINDINGS.md: *spec says X, API does Y, impact Z, test name* (prompt 4 helps)
- [ ] Group by **root cause**

## Minutes 24–27: WRAP UP
- [ ] Headline: **"N tests, N failing, from N bugs. Worst two are…"**
- [ ] Point at `.github/workflows/api-tests.yml`: "This runs on every change."

## 🛑 STOP CODING AT MINUTE 27

---

## Walkthrough (5–10 min)
1. **Headline:** numbers, worst two bugs, one spec question
2. **Framework:** env config, one client, curl repro in failures, valid-body setup, table-driven boundaries
3. **Runs on every change:** smoke first, then full suite, reports; known bugs tracked with `xfail(strict=True)`
4. **Next:** contract tests, clock injection for time-based cases, load test
5. **Language:** *"Python for speed today; at Ohme I'd build this in Kotlin with JUnit 5 and RestAssured."*

## AI workflow question (5–10 min)
- **"AI writes, triages and explores; deterministic tests decide what ships; a person approves anything that changes the suite."**
- Your honest example from the task: where AI helped, and where you caught it wrong.
