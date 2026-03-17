#!/usr/bin/env python3
"""
Detect the i18n framework and library in the current project.
Scans common config files and package manifests.

Usage: python detect_framework.py [project_root]
Output: JSON with detected framework, library, and locale file paths.
"""

import json
import os
import sys
from pathlib import Path


def detect(root: str = ".") -> dict:
    root = Path(root)
    result = {"framework": None, "library": None, "locale_paths": [], "config_files": []}

    # Next.js detection
    next_configs = list(root.glob("next.config.*"))
    if next_configs:
        result["framework"] = "nextjs"
        result["config_files"].extend(str(c) for c in next_configs)

        # Check for next-intl
        pkg = _read_package_json(root)
        if pkg and "next-intl" in str(pkg.get("dependencies", {})):
            result["library"] = "next-intl"
            messages_dir = root / "messages"
            if messages_dir.exists():
                result["locale_paths"] = sorted(str(f) for f in messages_dir.glob("*.json"))

    # React (Vite/CRA) detection
    elif list(root.glob("vite.config.*")) or _has_dep(root, "react"):
        result["framework"] = "react"
        if _has_dep(root, "react-i18next"):
            result["library"] = "react-i18next"
            locales_dir = root / "public" / "locales"
            if locales_dir.exists():
                result["locale_paths"] = sorted(
                    str(d) for d in locales_dir.iterdir() if d.is_dir()
                )

    # Flutter detection
    elif (root / "pubspec.yaml").exists():
        result["framework"] = "flutter"
        result["library"] = "arb"
        l10n_dir = root / "lib" / "l10n"
        if l10n_dir.exists():
            result["locale_paths"] = sorted(str(f) for f in l10n_dir.glob("*.arb"))

    # Rails detection
    elif (root / "Gemfile").exists():
        result["framework"] = "rails"
        result["library"] = "rails-i18n"
        locales_dir = root / "config" / "locales"
        if locales_dir.exists():
            result["locale_paths"] = sorted(str(f) for f in locales_dir.glob("*.yml"))

    # iOS detection
    elif list(root.rglob("*.xcodeproj")) or (root / "Package.swift").exists():
        result["framework"] = "ios"
        result["library"] = "strings"
        result["locale_paths"] = sorted(str(f) for f in root.rglob("*.lproj"))

    return result


def _read_package_json(root: Path) -> dict | None:
    pkg_path = root / "package.json"
    if pkg_path.exists():
        with open(pkg_path) as f:
            return json.load(f)
    return None


def _has_dep(root: Path, dep: str) -> bool:
    pkg = _read_package_json(root)
    if not pkg:
        return False
    all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    return dep in all_deps


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect(project_root)
    print(json.dumps(result, indent=2))
