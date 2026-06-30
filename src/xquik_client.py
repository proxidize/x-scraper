from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

XQUIK_SEARCH_URL = "https://xquik.com/api/v1/x/tweets/search"


def build_search_url(
    query: str,
    *,
    query_type: str = "Latest",
    cursor: str | None = None,
    limit: int | None = None,
    base_url: str = XQUIK_SEARCH_URL,
) -> str:
    params: dict[str, str] = {"q": query, "queryType": query_type}
    if cursor:
        params["cursor"] = cursor
    if limit is not None:
        params["limit"] = str(limit)
    return f"{base_url}?{urlencode(params)}"


def build_request(url: str, api_key: str) -> Request:
    return Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="GET",
    )


def normalize_search_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    tweets = payload.get("tweets") or payload.get("data") or []
    if not isinstance(tweets, list):
        tweets = []
    next_cursor = payload.get("next_cursor") or payload.get("nextCursor")
    return {
        "tweets": tweets,
        "tweet_count": len(tweets),
        "next_cursor": next_cursor if isinstance(next_cursor, str) else None,
    }


def search(
    query: str,
    *,
    api_key: str,
    query_type: str = "Latest",
    cursor: str | None = None,
    limit: int | None = None,
    opener: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    url = build_search_url(
        query,
        query_type=query_type,
        cursor=cursor,
        limit=limit,
    )
    request = build_request(url, api_key)
    with opener(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("Xquik search response must be a JSON object")
    return normalize_search_payload(payload)
