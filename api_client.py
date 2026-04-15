import os
import requests
from typing import Any, Dict, Optional


class ApiClient:
    """Minimal reusable HTTP client for a generic API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url or os.getenv("API_BASE_URL")
        if not self.base_url:
            raise ValueError("API_BASE_URL is required")

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            params=params,
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.request("POST", path, json=json)


def main() -> None:
    client = ApiClient()
    print("API client initialized")
    print("Set API_BASE_URL and optionally API_KEY in the environment.")
    print("Use client.get(path) or client.post(path, json=payload) to call the API.")


if __name__ == "__main__":
    main()
