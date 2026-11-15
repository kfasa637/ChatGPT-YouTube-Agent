# ChatGPT YouTube Agent

A practical starter kit for a YouTube creator assistant that works in two places:

1. **ChatGPT Custom GPT** — use `GPT_INSTRUCTIONS.md` as the GPT's Instructions and upload the skill files as Knowledge.
2. **GitHub/Python project** — use the optional command-line toolkit in `src/`.

This is an original implementation inspired by common YouTube creator workflows. It is not affiliated with or copied from another repository.

## Included workflows

`/yt-script`, `/yt-package`, `/yt-edit`, `/yt-comment`, `/yt-plan`, `/yt-viral`, `/yt-retention`, `/yt-shorts`, `/yt-seo`, `/yt-chapters`, `/yt-audit`.

In ChatGPT, type the command name in a message (for example `/yt-script`) and provide the topic/context. These are prompt conventions, not native slash-command registrations.

## Quick start: ChatGPT

1. Create a Custom GPT in ChatGPT's GPT builder.
2. Paste `GPT_INSTRUCTIONS.md` into the Instructions field.
3. Upload the Markdown files in `skills/` as Knowledge.
4. Enable web search and data analysis if those capabilities are available in your GPT builder.
5. For channel-specific analysis, provide a channel URL and any available analytics export. Do not share passwords or private login codes.

## Quick start: Python CLI

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -e .
youtube-agent --help
```

Optional YouTube Data API access:

```bash
# Windows PowerShell
$env:YOUTUBE_API_KEY="YOUR_KEY"

# macOS/Linux
export YOUTUBE_API_KEY="YOUR_KEY"
```

Then:

```bash
youtube-agent search "minecraft bedwars tips" --limit 5
youtube-agent stats "VIDEO_ID"
```

The API key is read from an environment variable; never commit it to GitHub.

## Important limits

- Public YouTube metadata can be queried through the YouTube Data API when a valid API key is configured.
- Private Studio analytics are not available from a public video ID. Supply your own CSV/export for retention and channel analytics.
- The agent must distinguish verified facts from estimates and creative hypotheses.
- Trend claims require current sources and dates. Never fabricate view counts, retention percentages, or competitor analytics.
