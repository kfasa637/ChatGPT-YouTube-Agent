from __future__ import annotations

import argparse
import json
from .youtube_api import search_videos, video_stats, YouTubeAPIError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="youtube-agent",
        description="ChatGPT YouTube Agent — public YouTube research helpers."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Search public YouTube videos.")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)

    stats = sub.add_parser("stats", help="Fetch public statistics for one video ID.")
    stats.add_argument("video_id")

    args = parser.parse_args()
    try:
        if args.command == "search":
            result = search_videos(args.query, args.limit)
        else:
            result = video_stats(args.video_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except YouTubeAPIError as exc:
        parser.exit(2, f"Error: {exc}\\n")


if __name__ == "__main__":
    main()
