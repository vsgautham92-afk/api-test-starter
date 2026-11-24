"""Thin HTTP client: one place for base URL, auth, timeouts and retries.

Auth per call (so auth tests are one line):
    api.get("/x")                      # default: Bearer <API_TOKEN> if set
    api.get("/x", auth=False)          # no Authorization header
    api.get("/x", auth="Bearer wrong") # custom header value
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Retry only *connection-level* drops (e.g. a server closing a keep-alive socket after a 500),
# and only for idempotent methods. HTTP status codes are never retried: a 500 must stay a 500.
_RETRY = Retry(total=2, connect=2, read=2, status=0, backoff_factor=0.1,
               allowed_methods=frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"}),
               raise_on_status=False)


class ApiClient:
    def __init__(self, base_url: str, token: str | None = None, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        adapter = HTTPAdapter(max_retries=_RETRY)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _auth_headers(self, auth: bool | str) -> dict:
        if auth is True:
            return {"Authorization": f"Bearer {self.token}"} if self.token else {}
        if isinstance(auth, str):
            return {"Authorization": auth}
        return {}

    def request(self, method: str, path: str, auth: bool | str = True, headers: dict | None = None,
                **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        merged = {**self._auth_headers(auth), **(headers or {})}
        if "data" in kwargs and kwargs["data"] is not None:
            merged.setdefault("Content-Type", "application/json")  # for broken-JSON tests
        return self.session.request(method, f"{self.base_url}{path}", headers=merged, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
