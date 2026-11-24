"""Proves the framework runs end to end before any real tests are written."""
import pytest
import requests


@pytest.mark.smoke
def test_service_is_reachable(api, base_url):
    try:
        resp = api.get("/")
    except requests.ConnectionError:
        pytest.fail(f"Cannot reach the API at {base_url}. Is it running? Is BASE_URL right?")
    assert resp.status_code < 500, f"Service answered {resp.status_code} at {base_url}/"
