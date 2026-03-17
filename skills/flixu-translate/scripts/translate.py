#!/usr/bin/env python3
"""
Translate locale files using the Flixu API.
Supports JSON (flat and nested) i18n files.

Usage: python translate.py <source_file> <target_langs> [--api-key KEY]
Example: python translate.py messages/en.json "de,fr,es"

Output: Translated files written to the same directory as the source.

Environment: FLIXU_API_KEY must be set (or pass --api-key).
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError


API_BASE = "https://api.flixu.ai/v1"


def translate_batch(strings: dict, source_lang: str, target_langs: list[str], api_key: str) -> dict:
    """Call POST /v1/translate/batch."""
    payload = json.dumps({
        "strings": strings,
        "source_lang": source_lang,
        "target_langs": target_langs,
    }).encode()

    req = Request(
        f"{API_BASE}/translate/batch",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(req) as resp:
            result = json.loads(resp.read())
            return result.get("data", {}).get("translations", {})
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"API error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def flatten_json(data: dict, prefix: str = "") -> dict[str, str]:
    """Flatten nested JSON to dot-notation keys."""
    items = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            items.update(flatten_json(value, full_key))
        else:
            items[full_key] = str(value)
    return items


def unflatten_json(flat: dict[str, str]) -> dict:
    """Reconstruct nested JSON from dot-notation keys."""
    result = {}
    for key, value in flat.items():
        parts = key.split(".")
        current = result
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value
    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: python translate.py <source_file> <target_langs> [--api-key KEY]")
        print('Example: python translate.py messages/en.json "de,fr,es"')
        sys.exit(1)

    source_path = Path(sys.argv[1])
    target_langs = [l.strip() for l in sys.argv[2].split(",")]
    api_key = os.environ.get("FLIXU_API_KEY")

    if "--api-key" in sys.argv:
        api_key = sys.argv[sys.argv.index("--api-key") + 1]

    if not api_key:
        print("Error: FLIXU_API_KEY not set. Pass --api-key or set environment variable.", file=sys.stderr)
        sys.exit(1)

    # Read and flatten source
    with open(source_path) as f:
        source_data = json.load(f)

    flat_strings = flatten_json(source_data)
    source_lang = source_path.stem  # en.json → en

    print(f"Translating {len(flat_strings)} strings from '{source_lang}' to {target_langs}...")

    # Call API
    translations = translate_batch(flat_strings, source_lang, target_langs, api_key)

    # Write output files
    output_dir = source_path.parent
    for lang, translated_flat in translations.items():
        nested = unflatten_json(translated_flat)
        output_path = output_dir / f"{lang}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(nested, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {output_path} ({len(translated_flat)} strings)")

    print(f"\nDone! Translated to {len(translations)} languages.")


if __name__ == "__main__":
    main()
