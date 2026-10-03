#!/usr/bin/env python3
"""
render-wotd.py
Fetates the curated multi-source Word of the Day from the Castles-in-the-Sky API
and formats the definitions, etymologies, examples, and enrichment quotes
into the target staging Markdown file.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

WOTD_ENDPOINT: str = "https://api.castles-in-the-sky.org/wotd/all"
SOURCE_ORDER: dict[str, int] = {
    "Dictionary.com": 1,
    "Britannica": 2,
    "Merriam-Webster": 3,
}


def fetch_words(api_key: str) -> list[dict] | None:
    """Fetch all Word of the Day entries from the API."""
    if not api_key:
        print("Notice: CASTLE_KEY not provided. Skipping Word of the Day section.", file=sys.stderr)
        return None

    req = urllib.request.Request(
        WOTD_ENDPOINT,
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "GitHubActions-README-Update/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list) and len(data) > 0:
                return [item for item in data if item is not None]
            print("Notice: Word of the Day response was empty. Skipping section.", file=sys.stderr)
            return None
    except Exception as exc:
        print(f"Notice: Failed to fetch Words of the Day ({exc}). Skipping section gracefully.", file=sys.stderr)
        return None


def format_examples(sentences: list[str]) -> list[str]:
    """Format blockquoted example sentences without dangling quote markers."""
    lines: list[str] = []
    valid = [s.strip() for s in sentences if s and s.strip()]
    for i, ex in enumerate(valid):
        lines.append(f"> _{ex}_")
        if i < len(valid) - 1:
            lines.append(">")
    return lines


def get_str(d: dict, key: str, default: str = "") -> str:
    """Safely get a string value from a dictionary, handling None/null values."""
    val = d.get(key)
    if val is None:
        return default
    return str(val).strip()


def format_source_section(item: dict) -> list[str]:
    """Format a single dictionary entry based on its source-specific schema."""
    lines: list[str] = []

    source: str = get_str(item, "source", "Word of the Day")
    word: str = get_str(item, "word")
    pos: str = get_str(item, "partOfSpeech")
    pronunciation: str = get_str(item, "pronunciation")
    definition: str = get_str(item, "definition")

    # Section heading
    lines.append(f"### {source}")
    lines.append("")

    # Word line: **word** _pos_ • /pronunciation/
    word_parts: list[str] = [f"**{word}**"]
    if pos:
        word_parts.append(f"_{pos}_")
    word_line: str = " ".join(word_parts)
    if pronunciation:
        word_line += f" • /{pronunciation}/"

    lines.append(word_line)
    lines.append("")

    if definition:
        lines.append(definition)
        lines.append("")

    # Source-specific enrichment
    if source == "Dictionary.com":
        explanation: str = get_str(item, "explanation")
        example: str = get_str(item, "example")

        if explanation:
            lines.append(explanation)
            lines.append("")

        if example:
            lines.append(f"> _{example}_")
            lines.append("")

    elif source == "Britannica":
        examples: list[str] = item.get("exampleSentences") or []
        ex_lines = format_examples(examples)
        if ex_lines:
            lines.extend(ex_lines)
            lines.append("")

        # Synonyms and Antonyms
        synonyms: list[str] = [s.strip() for s in (item.get("synonyms") or []) if s and str(s).strip()]
        antonyms: list[str] = [a.strip() for a in (item.get("antonyms") or []) if a and str(a).strip()]

        lex_parts: list[str] = []
        if synonyms:
            lex_parts.append(f"_Similar: {', '.join(synonyms)}_")
        if antonyms:
            lex_parts.append(f"_Opposite: {', '.join(antonyms)}_")

        if lex_parts:
            lines.append("  •  ".join(lex_parts))
            lines.append("")

        # Enrichment quote
        enrichment: dict = item.get("enrichment") or {}
        quote: str = get_str(enrichment, "quote")
        author: str = get_str(enrichment, "author")
        context_source: str = get_str(enrichment, "source")
        pub_date: str = get_str(enrichment, "publicationDate")

        if quote and author:
            lines.append(f"> _\"{quote}\"_")
            lines.append(">")
            citation = f"— **{author}**"
            if context_source:
                citation += f", {context_source}"
            if pub_date:
                citation += f" ({pub_date})"
            lines.append(f"> {citation}")
            lines.append("")

    elif source == "Merriam-Webster":
        examples: list[str] = item.get("exampleSentences") or []
        ex_lines = format_examples(examples)
        if ex_lines:
            lines.extend(ex_lines)
            lines.append("")

        in_context: str = get_str(item, "inContext")
        if in_context:
            lines.append(f"> {in_context}")
            lines.append("")

        did_you_know: str = get_str(item, "didYouKnow")
        if did_you_know:
            lines.append(f"_{did_you_know}_")
            lines.append("")

    return lines


def render_wotd(target_file: str, api_key: str) -> None:
    """Fetch Words of the Day and write/append markdown to target_file."""
    items = fetch_words(api_key)
    if not items:
        return

    # Sort items by curated editorial order
    items.sort(key=lambda x: SOURCE_ORDER.get(x.get("source", ""), 99))

    has_prior_content: bool = os.path.exists(target_file) and os.path.getsize(target_file) > 0
    now_utc: str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = []

    if has_prior_content:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Words of the Day")
    else:
        lines.append("# Words of the Day")
        lines.append("")
        lines.append(f"_Updated: {now_utc}_")

    lines.append("")

    for item in items:
        source_lines = format_source_section(item)
        lines.extend(source_lines)

    content: str = "\n".join(lines).rstrip() + "\n"

    with open(target_file, "a", encoding="utf-8") as f:
        f.write(content)

    print(f"Rendered Words of the Day ({len(items)} sources) to {target_file}")


def main() -> None:
    target: str = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TARGET_FILE", "README.md")
    api_key: str = os.environ.get("CASTLE_KEY", "")
    render_wotd(target, api_key)


if __name__ == "__main__":
    main()
