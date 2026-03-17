#!/usr/bin/env python3
"""
Audit translation key completeness and interpolation consistency across locale files.
Supports JSON (flat and nested) locale files.

Usage: python audit_keys.py <source_locale_file> <target_locale_dir>
Example: python audit_keys.py messages/en.json messages/

Output: Structured report with missing keys, extra keys, coverage %, and interpolation mismatches.
"""

import json
import re
import sys
from pathlib import Path


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


def extract_variables(text: str) -> set[str]:
    """Extract interpolation variables from a translation string."""
    patterns = [
        r"\{(\w+)\}",       # {name} — ICU
        r"\{\{(\w+)\}\}",   # {{name}} — Handlebars
        r"%\{(\w+)\}",      # %{name} — Ruby
        r"%[sd]",           # %s, %d — printf
        r"\$\{(\w+)\}",     # ${name} — JS template
    ]
    variables = set()
    for pattern in patterns:
        variables.update(re.findall(pattern, text))
    return variables


def audit(source_path: str, target_dir: str) -> dict:
    source = Path(source_path)
    target_dir = Path(target_dir)

    with open(source) as f:
        source_data = flatten_json(json.load(f))

    source_locale = source.stem
    results = {
        "source_locale": source_locale,
        "source_key_count": len(source_data),
        "locales": {},
        "interpolation_issues": [],
    }

    for target_file in sorted(target_dir.glob("*.json")):
        locale = target_file.stem
        if locale == source_locale:
            continue

        with open(target_file) as f:
            target_data = flatten_json(json.load(f))

        source_keys = set(source_data.keys())
        target_keys = set(target_data.keys())

        missing = sorted(source_keys - target_keys)
        extra = sorted(target_keys - source_keys)
        coverage = (len(target_keys & source_keys) / len(source_keys) * 100) if source_keys else 100

        results["locales"][locale] = {
            "key_count": len(target_keys),
            "missing_keys": missing,
            "extra_keys": extra,
            "coverage_percent": round(coverage, 1),
        }

        # Check interpolation consistency
        for key in source_keys & target_keys:
            source_vars = extract_variables(source_data[key])
            target_vars = extract_variables(target_data[key])
            if source_vars and source_vars != target_vars:
                results["interpolation_issues"].append({
                    "locale": locale,
                    "key": key,
                    "source_value": source_data[key],
                    "target_value": target_data[key],
                    "expected_vars": sorted(source_vars),
                    "actual_vars": sorted(target_vars),
                })

    return results


def print_report(results: dict):
    print(f"Translation Coverage Report")
    print(f"===========================")
    print(f"Source: {results['source_locale']} ({results['source_key_count']} keys)\n")

    print(f"| {'Locale':<8} | {'Keys':<6} | {'Missing':<8} | {'Extra':<6} | {'Coverage':<10} |")
    print(f"|{'-'*10}|{'-'*8}|{'-'*10}|{'-'*8}|{'-'*12}|")

    for locale, data in sorted(results["locales"].items()):
        print(f"| {locale:<8} | {data['key_count']:<6} | {len(data['missing_keys']):<8} | {len(data['extra_keys']):<6} | {data['coverage_percent']:<9}% |")

    # Missing keys detail
    for locale, data in sorted(results["locales"].items()):
        if data["missing_keys"]:
            print(f"\nMissing keys in '{locale}':")
            for key in data["missing_keys"][:20]:
                print(f"  - {key}")
            if len(data["missing_keys"]) > 20:
                print(f"  ... and {len(data['missing_keys']) - 20} more")

    # Interpolation issues
    if results["interpolation_issues"]:
        print(f"\nInterpolation Issues ({len(results['interpolation_issues'])} found):")
        for issue in results["interpolation_issues"][:10]:
            print(f"\n  ⚠ {issue['locale']}/{issue['key']}:")
            print(f"    Source: \"{issue['source_value']}\"")
            print(f"    Target: \"{issue['target_value']}\"")
            print(f"    Expected vars: {issue['expected_vars']}, got: {issue['actual_vars']}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python audit_keys.py <source_locale_file> <target_locale_dir>")
        print("Example: python audit_keys.py messages/en.json messages/")
        sys.exit(1)

    results = audit(sys.argv[1], sys.argv[2])
    print_report(results)

    # Also output JSON for programmatic use
    json_path = Path(sys.argv[2]) / ".audit_report.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nJSON report saved to: {json_path}")
