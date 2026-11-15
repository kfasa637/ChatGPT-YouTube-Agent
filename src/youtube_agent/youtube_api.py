from __future__ import annotations

import os
from typing import Any
import requests

BASE = "https://www.googleapis.com/youtube/v3"


class YouTubeAPIError(RuntimeError):
    pass


def _api_key() -> str:
    key = os.getenv("YOUTUBE_API_KEY", "").strip()
    if not key:
        raise YouTubeAPIError(
            "YOUTUBE_API_KEY is not set. Create an API key in Google Cloud "
            "and set it as an environment variable; never commit it to GitHub."
        )
    return key


def _get(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    query = {"key": _api_key(), **params}
    response = requests.get(f"{BASE}/{endpoint}", params=query, timeout=20)
    if response.status_code != 200:
        try:
            message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            message = response.text
        raise YouTubeAPIError(f"YouTube API error ({response.status_code}): {message}")
    return response.json()


def search_videos(query: str, limit: int = 5) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit), 50))
    data = _get("search", {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": limit,
        "order": "relevance",
    })
    results = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        results.append({
            "video_id": item.get("id", {}).get("videoId"),
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description", ""),
            "url": f"https://www.youtube.com/watch?v={item.get('id', {}).get('videoId')}",
        })
    return results


def video_stats(video_id: str) -> dict[str, Any]:
    data = _get("videos", {
        "part": "snippet,statistics,contentDetails",
        "id": video_id,
    })
    items = data.get("items", [])
    if not items:
        raise YouTubeAPIError(f"No public video found for ID: {video_id}")
    item = items[0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    return {
        "video_id": video_id,
        "title": snippet.get("title"),
        "channel": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "duration": item.get("contentDetails", {}).get("duration"),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats["likeCount"]) if "likeCount" in stats else None,
        "comments": int(stats["commentCount"]) if "commentCount" in stats else None,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "note": "Public counters only; this does not include private YouTube Studio retention or CTR.",
    }
