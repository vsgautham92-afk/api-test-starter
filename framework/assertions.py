"""Assertions that turn a failing test into a bug report: what came back + a curl repro."""
import json
import shlex

import requests


def as_curl(resp: requests.Response) -> str:
    """Rebuild the request as a copy-pasteable curl command."""
    req = resp.request
    parts = ["curl", "-i", "-X", req.method]
    for key, value in req.headers.items():
        if key.lower() in ("authorization", "content-type"):
            parts += ["-H", f"{key}: {value}"]
    if req.body:
        body = req.body.decode() if isinstance(req.body, bytes) else req.body
        parts += ["-d", body]
    parts.append(req.url)
    return " ".join(shlex.quote(p) for p in parts)


def explain(resp: requests.Response) -> str:
    try:
        body = json.dumps(resp.json(), indent=2)
    except ValueError:
        body = resp.text
    return f"\n  got {resp.status_code}: {body[:1200]}\n  repro: {as_curl(resp)}"


def assert_status(resp: requests.Response, expected: int):
    assert resp.status_code == expected, f"Expected HTTP {expected}.{explain(resp)}"


def json_body(resp: requests.Response):
    try:
        return resp.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON.{explain(resp)}")
