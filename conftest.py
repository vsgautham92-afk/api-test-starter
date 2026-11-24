"""
Shared fixtures. Configure with environment variables:

    BASE_URL   where the API under test runs   (default http://localhost:8000)
    API_TOKEN  bearer token, if the API needs one
    SPEC_PATH  path to an OpenAPI file          (optional; enables schema checks by name)
"""
import os

import pytest

from framework.api_client import ApiClient
from framework.schema import load_spec


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api(base_url) -> ApiClient:
    return ApiClient(base_url, token=os.getenv("API_TOKEN"))


@pytest.fixture(scope="session")
def spec():
    path = os.getenv("SPEC_PATH")
    return load_spec(path) if path else None


# Valid-body factory: every POST test starts from a body the spec accepts and overrides ONE
# field, so each failure has exactly one cause. Fill VALID_BODY in from the spec on the day.
VALID_BODY: dict = {
    # "chargerId": "CHG-0001",
    # "targetSocPercent": 80,
}


@pytest.fixture
def valid_body():
    def _make(**overrides):
        body = dict(VALID_BODY)
        body.update(overrides)
        return body
    return _make
