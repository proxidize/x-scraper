from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "xquik_client.py"
SPEC = importlib.util.spec_from_file_location("xquik_client", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
xquik_client = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(xquik_client)

build_request = xquik_client.build_request
build_search_url = xquik_client.build_search_url
normalize_search_payload = xquik_client.normalize_search_payload
search = xquik_client.search


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_build_search_url_uses_public_search_route():
    url = build_search_url("historical search", cursor="next", limit=10)

    assert url == (
        "https://xquik.com/api/v1/x/tweets/search?"
        "q=historical+search&queryType=Latest&cursor=next&limit=10"
    )


def test_build_request_sets_bearer_header():
    request = build_request("https://example.test/search", "test-key")

    assert request.headers["Accept"] == "application/json"
    assert request.headers["Authorization"] == "Bearer test-key"


def test_normalize_search_payload_supports_tweets_or_data():
    assert normalize_search_payload({"tweets": [{"id": "1"}], "next_cursor": "n"}) == {
        "tweets": [{"id": "1"}],
        "tweet_count": 1,
        "next_cursor": "n",
    }
    assert normalize_search_payload({"data": [{"id": "2"}], "nextCursor": "m"})[
        "next_cursor"
    ] == "m"


def test_search_uses_injected_opener():
    captured = {}

    def fake_opener(request, *, timeout):
        captured["url"] = request.full_url
        captured["authorization"] = request.headers["Authorization"]
        captured["timeout"] = timeout
        return FakeResponse({"tweets": [{"id": "1"}]})

    result = search("mcp", api_key="test-key", opener=fake_opener)

    assert result["tweet_count"] == 1
    assert captured == {
        "url": "https://xquik.com/api/v1/x/tweets/search?q=mcp&queryType=Latest",
        "authorization": "Bearer test-key",
        "timeout": 30,
    }


def test_search_rejects_non_object_payload():
    def fake_opener(_request, *, timeout):
        return FakeResponse(["not-object"])

    with pytest.raises(ValueError, match="JSON object"):
        search("mcp", api_key="test-key", opener=fake_opener)
