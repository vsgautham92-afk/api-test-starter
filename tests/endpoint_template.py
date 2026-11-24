"""
TEMPLATE: copy to tests/test_<endpoint>.py and fill in from the spec. (Not collected as-is.)

Work down the layers in order and stop when time runs out. Each layer finds a different
kind of bug, so do one or two tests per layer rather than twenty in the first.
  1 contract  2 business rules  3 boundaries  4 types/missing  5 auth  6 across endpoints
  7 data sanity (fields that must agree)  8 quick non-functional (unknown route, wrong method)
"""
import pytest

from framework.assertions import assert_status, explain, json_body
from framework.schema import assert_matches_schema

PATH = "/things"
SCHEMA = {  # transcribe from the spec, or use "SchemaName" with SPEC_PATH
    "type": "object",
    "required": [],
    "properties": {},
}


# 1. Contract + happy path
@pytest.mark.smoke
@pytest.mark.contract
def test_create_returns_201_and_matches_contract(api, valid_body):
    r = api.post(PATH, json=valid_body())
    assert_status(r, 201)
    assert r.headers.get("Content-Type", "").startswith("application/json"), explain(r)
    assert_matches_schema(json_body(r), SCHEMA)


# 2. Business rules: one test per "must" in the spec. Recalculate derived values yourself.
@pytest.mark.contract
def test_total_equals_sum_of_parts(api, valid_body):
    body = json_body(api.post(PATH, json=valid_body()))
    assert body["total"] == pytest.approx(sum(p["value"] for p in body["parts"]), abs=0.01)


# 3. Boundaries: min and max ACCEPTED, min-1 and max+1 REJECTED, and the "equal" case for > rules
@pytest.mark.boundary
@pytest.mark.parametrize("value, expected", [(0, 400), (1, 201), (100, 201), (101, 400)])
def test_value_boundaries(api, valid_body, value, expected):
    assert_status(api.post(PATH, json=valid_body(value=value)), expected)


# 4. Types and missing fields. Any 500 is a finding.
@pytest.mark.negative
@pytest.mark.parametrize("bad", ["60", None, True, -1], ids=["string", "null", "bool", "negative"])
def test_wrong_types_rejected(api, valid_body, bad):
    assert_status(api.post(PATH, json=valid_body(value=bad)), 400)


@pytest.mark.negative
@pytest.mark.parametrize("missing", ["value"])  # list every required field
def test_missing_field_rejected(api, valid_body, missing):
    body = valid_body()
    del body[missing]
    assert_status(api.post(PATH, json=body), 400)


@pytest.mark.negative
def test_broken_json_rejected(api):
    assert_status(api.post(PATH, data="{not json"), 400)


# 5. Auth: test EACH endpoint separately
@pytest.mark.security
@pytest.mark.parametrize("auth", [False, "Bearer wrong", "wrong-no-prefix"], ids=["missing", "wrong", "no-bearer"])
def test_requires_auth(api, auth):
    assert_status(api.get(f"{PATH}/1", auth=auth), 401)


# 6. Across endpoints: write with one, read with the other ("test BOTH endpoints" is a hint)
@pytest.mark.integration
def test_created_thing_is_visible_on_the_other_endpoint(api, valid_body):
    created = json_body(api.post(PATH, json=valid_body()))
    fetched = api.get(f"/parents/{created['parentId']}")
    assert json_body(fetched)["latestThingId"] == created["id"], explain(fetched)


# Known bug that's ticketed: keep the pipeline green but the bug visible.
# strict=True means that when someone fixes it, this test FAILS, forcing the marker off.
@pytest.mark.xfail(strict=True, reason="BUG-02 / JIRA-123: returns 200 instead of 201")
def test_known_bug_example(api, valid_body):
    assert_status(api.post(PATH, json=valid_body()), 201)
