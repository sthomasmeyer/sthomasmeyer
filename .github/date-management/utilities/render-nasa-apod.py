#!/usr/bin/env python3
"""
render-nasa-apod.py
Fetches the latest Astronomy Picture of the Day (APOD) from NASA Science's
official REST endpoint (https://science.nasa.gov/wp-json/wp/v2/apod-basic)
and appends formatted Markdown to the target staging file.
Supports both image and video media types.
"""

from __future__ import annotations

import html as html_module
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

APOD_ENDPOINT: str = "https://science.nasa.gov/wp-json/wp/v2/apod-basic?per_page=1"
USER_AGENT: str = "GitHubActions-README-Update/1.0"


def clean_html_explanation(raw_html: str) -> str:
    """Strip HTML tags, extraneous submission notices, and normalize whitespace."""
    if not raw_html:
        return ""

    # Remove leading Explanation: tag if present
    text: str = re.sub(
        r"^\s*<[^>]+>\s*Explanation:?\s*</[^>]+>\s*",
        "",
        raw_html,
        flags=re.IGNORECASE,
    )

    # Remove trailing metadata (e.g., Tomorrow's picture or submission notices)
    text = re.split(
        r"<br\s*/?>\s*<strong>\s*(Tomorrow|APOD)",
        text,
        flags=re.IGNORECASE,
    )[0]

    # Convert line breaks and paragraph tags into newlines
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</p>\s*<p>", "\n\n", text)

    # Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape HTML entities (e.g. &nbsp;, &amp;, &quot;)
    text = html_module.unescape(text)

    # Normalize excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def fetch_apod() -> dict[str, str] | None:
    """Fetch the latest APOD item from NASA Science."""
    req = urllib.request.Request(APOD_ENDPOINT, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            print("Notice: Unexpected APOD response structure. Skipping section.", file=sys.stderr)
            return None
    except Exception as exc:
        print(f"Notice: Failed to fetch NASA APOD ({exc}). Skipping section gracefully.", file=sys.stderr)
        return None


def render_apod(target_file: str) -> None:
    """Fetch APOD and write/append markdown to target_file."""
    item = fetch_apod()
    if not item:
        return

    title: str = (item.get("title") or "NASA Astronomy Picture of the Day").strip()
    media_type: str = (item.get("media_type") or "image").lower()
    image_url: str = (item.get("hdurl") or item.get("url") or "").strip()
    permalink: str = (item.get("permalink") or item.get("url") or "").strip()
    raw_explanation: str = item.get("explanation") or ""
    explanation: str = clean_html_explanation(raw_explanation)

    # Check whether the target staging file already has content (e.g. Notable Date leads)
    has_prior_content: bool = os.path.exists(target_file) and os.path.getsize(target_file) > 0

    now_utc: str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = []

    if has_prior_content:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## NASA Astronomy Picture of the Day")
    else:
        lines.append("# NASA Astronomy Picture of the Day")
        lines.append("")
        lines.append(f"_Updated: {now_utc}_")

    lines.append("")
    lines.append(f"### {title}")
    lines.append("")

    if media_type == "video":
        if image_url:
            lines.append(f"[![{title}]({image_url})]({permalink})")
            lines.append("")
        lines.append(f"▶️ _[Watch today's Astronomy Video on NASA Science]({permalink})_")
        lines.append("")
    else:
        if image_url:
            lines.append(f"![{title}]({image_url})")
            lines.append("")

    if explanation:
        lines.append(explanation)
        lines.append("")

    content: str = "\n".join(lines) + "\n"

    with open(target_file, "a", encoding="utf-8") as f:
        f.write(content)

    print(f"Rendered NASA APOD: '{title}' ({media_type}) to {target_file}")


def main() -> None:
    target: str = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TARGET_FILE", "README.md")
    render_apod(target)


if __name__ == "__main__":
    main()
