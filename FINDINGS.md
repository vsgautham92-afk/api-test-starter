# Findings: spec vs actual behaviour

**Headline:** _N tests, N failing, from N root causes. The two I'd fix today are ... _

Severity, in EV home-charging terms:
**High** = car not charged by morning, wrong price, can't do a common action (charge to 100%), security or privacy hole ·
**Medium** = unhandled 500, data inconsistent between endpoints, a silent no-op the user thinks worked ·
**Low** = contract detail (200 vs 201, missing header, timestamp format, type coercion)

## Product bugs (the spec is clear and the API breaks it)
Write each as: spec says X, API does Y, impact is Z, repro is the curl from the test output.

| ID | Sev | Endpoint | Spec says | API does | Impact | Test |
|---|---|---|---|---|---|---|
| BUG-01 | | | | | | |
| BUG-02 | | | | | | |

## Spec questions (the spec is silent or ambiguous: ask, don't guess, don't hard-code a guess)
1.

## Test limitations (what I couldn't test and what I'd need)
-

## With more time
-
