#!/usr/bin/env python3
"""
Detect the current translation provider in a project.
Scans package.json, env files, and source code for provider-specific patterns.

Usage: python detect_provider.py [project_root]
Output: JSON with detected provider, library, env vars, and API call locations.
"""

import json
import os
import re
import sys
from pathlib import Path


PROVIDERS = {
    "deepl": {
        "packages": ["deepl-node", "deepl"],
        "env_vars": ["DEEPL_AUTH_KEY", "DEEPL_API_KEY"],
        "imports": ["deepl-node", "deepl"],
        "api_patterns": [r"api-free\.deepl\.com", r"api\.deepl\.com"],
    },
    "google": {
        "packages": ["@google-cloud/translate", "google-translate-api"],
        "env_vars": ["GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_TRANSLATE_API_KEY"],
        "imports": ["@google-cloud/translate", "google-translate-api"],
        "api_patterns": [r"translate\.googleapis\.com"],
    },
    "lokalise": {
        "packages": ["@lokalise/node-api", "lokalise-cli"],
        "env_vars": ["LOKALISE_API_TOKEN", "LOKALISE_PROJECT_ID"],
        "imports": ["@lokalise/node-api"],
        "api_patterns": [r"api\.lokalise\.com"],
    },
    "phrase": {
        "packages": ["phrase-cli"],
        "env_vars": ["PHRASE_ACCESS_TOKEN"],
        "imports": [],
        "api_patterns": [r"api\.phrase\.com"],
        "config_files": [".phrase.yml"],
    },
    "aws": {
        "packages": ["@aws-sdk/client-translate"],
        "env_vars": ["AWS_ACCESS_KEY_ID"],
        "imports": ["@aws-sdk/client-translate", "TranslateClient"],
        "api_patterns": [r"translate\.amazonaws\.com"],
    },
}


def detect(root: str = ".") -> dict:
    root = Path(root)
    result = {
        "provider": None,
        "library": None,
        "env_vars_found": [],
        "api_call_locations": [],
        "config_files": [],
    }

    # Check package.json
    pkg = _read_package_json(root)
    all_deps = {}
    if pkg:
        all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

    # Check env files
    env_vars = _read_env_files(root)

    # Scan for each provider
    for provider_name, signals in PROVIDERS.items():
        # Check packages
        for pkg_name in signals["packages"]:
            if pkg_name in all_deps:
                result["provider"] = provider_name
                result["library"] = f"{pkg_name}@{all_deps[pkg_name]}"
                break

        # Check env vars
        for var in signals["env_vars"]:
            if var in env_vars:
                result["env_vars_found"].append(var)
                if not result["provider"]:
                    result["provider"] = provider_name

        # Check config files
        for config_file in signals.get("config_files", []):
            if (root / config_file).exists():
                result["config_files"].append(config_file)
                if not result["provider"]:
                    result["provider"] = provider_name

        if result["provider"]:
            # Find API call locations in source files
            for pattern in signals["api_patterns"]:
                result["api_call_locations"].extend(
                    _grep_files(root, pattern, extensions=[".ts", ".js", ".tsx", ".jsx", ".py"])
                )
            break

    return result


def _read_package_json(root: Path) -> dict | None:
    pkg_path = root / "package.json"
    if pkg_path.exists():
        with open(pkg_path) as f:
            return json.load(f)
    return None


def _read_env_files(root: Path) -> set[str]:
    env_vars = set()
    for env_file in [".env", ".env.local", ".env.example", ".env.development"]:
        path = root / env_file
        if path.exists():
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        env_vars.add(line.split("=")[0])
    return env_vars


def _grep_files(root: Path, pattern: str, extensions: list[str]) -> list[str]:
    matches = []
    for ext in extensions:
        for file in root.rglob(f"*{ext}"):
            if "node_modules" in str(file) or ".git" in str(file):
                continue
            try:
                content = file.read_text(errors="ignore")
                if re.search(pattern, content):
                    matches.append(str(file.relative_to(root)))
            except Exception:
                pass
    return matches


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect(project_root)
    print(json.dumps(result, indent=2))
