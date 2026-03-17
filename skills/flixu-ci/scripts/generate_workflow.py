#!/usr/bin/env python3
"""
Generate CI/CD workflow files for auto-translating locale files.

Usage: python generate_workflow.py --platform github|gitlab --source messages/en.json --langs "de,fr,es"
Output: Writes the workflow file to the correct location (.github/workflows/ or .gitlab-ci.yml).
"""

import argparse
import os
import sys
from pathlib import Path


GITHUB_TEMPLATE = """name: Flixu Auto-Translate

on:
  push:
    branches: [{branches}]
    paths:
      - '{source_path}'

permissions:
  contents: write
  pull-requests: write

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Detect changed strings
        id: changes
        run: |
          git diff HEAD~1 --name-only | grep -E '{source_pattern}' > changed_files.txt
          if [ -s changed_files.txt ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Translate to target locales
        if: steps.changes.outputs.has_changes == 'true'
        env:
          FLIXU_API_KEY: ${{{{ secrets.FLIXU_API_KEY }}}}
        run: |
          TARGET_LANGS="{langs}"
          for lang in $TARGET_LANGS; do
            echo "Translating to $lang..."
            curl -s -X POST https://api.flixu.ai/v1/translate/batch \\
              -H "Authorization: Bearer $FLIXU_API_KEY" \\
              -H "Content-Type: application/json" \\
              -d @<(jq -n \\
                --argjson strings "$(cat {source_path})" \\
                --arg source_lang "{source_lang}" \\
                --arg target_lang "$lang" \\
                '{{strings: $strings, source_lang: $source_lang, target_langs: [$target_lang]}}' \\
              ) | jq ".data.translations.${{lang}}" > "{output_dir}/${{lang}}.json"
          done

      - name: Create Pull Request
        if: steps.changes.outputs.has_changes == 'true'
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{{{ secrets.GITHUB_TOKEN }}}}
          commit-message: "chore(i18n): auto-translate updated strings"
          title: "🌐 Auto-translated strings"
          body: |
            Automatically translated changed strings from `{source_lang}`.
            **Target locales**: {langs}
          branch: i18n/auto-translate
          labels: i18n, automated
"""

GITLAB_TEMPLATE = """translate:
  stage: deploy
  image: curlimages/curl:latest
  only:
    changes:
      - {source_path}
  script:
    - |
      TARGET_LANGS="{langs}"
      for lang in $TARGET_LANGS; do
        curl -s -X POST https://api.flixu.ai/v1/translate/batch \\
          -H "Authorization: Bearer $FLIXU_API_KEY" \\
          -H "Content-Type: application/json" \\
          -d '{{"strings": '$(cat {source_path})', "source_lang": "{source_lang}", "target_langs": ["'$lang'"]}}' \\
          | jq ".data.translations.${{lang}}" > "{output_dir}/${{lang}}.json"
      done
    - git add {output_dir}/
    - git commit -m "chore(i18n): auto-translate" || true
    - git push
  variables:
    FLIXU_API_KEY: $FLIXU_API_KEY
"""


def main():
    parser = argparse.ArgumentParser(description="Generate Flixu CI/CD translation workflow")
    parser.add_argument("--platform", choices=["github", "gitlab"], required=True)
    parser.add_argument("--source", required=True, help="Source locale file path (e.g., messages/en.json)")
    parser.add_argument("--langs", required=True, help="Comma-separated target languages (e.g., de,fr,es)")
    parser.add_argument("--branches", default="main", help="Trigger branches (default: main)")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()

    source = Path(args.source)
    source_lang = source.stem
    output_dir = str(source.parent)
    source_pattern = str(source).replace(".", r"\\.")
    langs = " ".join(l.strip() for l in args.langs.split(","))

    config = {
        "source_path": str(source),
        "source_pattern": source_pattern,
        "source_lang": source_lang,
        "output_dir": output_dir,
        "langs": langs,
        "branches": args.branches,
    }

    if args.platform == "github":
        content = GITHUB_TEMPLATE.format(**config)
        output_path = Path(".github/workflows/flixu-translate.yml")
    else:
        content = GITLAB_TEMPLATE.format(**config)
        output_path = Path(".gitlab-ci-translate.yml")

    if args.dry_run:
        print(content)
        print(f"\n# Would write to: {output_path}")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        print(f"✓ Wrote {output_path}")
        print(f"  Source: {source}")
        print(f"  Target languages: {langs}")
        print(f"  Trigger: push to {args.branches}")
        print(f"\nRemember to add FLIXU_API_KEY as a repository secret!")


if __name__ == "__main__":
    main()
