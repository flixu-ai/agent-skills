---
name: flixu-ci
description: Generate CI/CD pipeline configurations that automate translation on every push. Use this skill when a developer asks to "automate translations", "add translation to CI", "create GitHub Action for translation", "create GitLab CI for i18n", "auto-translate on push", "translation pipeline", "localization workflow automation", or any request involving automating the translation of locale files as part of a CI/CD workflow. Also triggers on "translation PR", "auto-localize", "continuous localization", or even just "I don't want to manually translate anymore". If a developer has locale files and wants them auto-translated when the source changes, this is the right skill.
---

# Flixu CI

Generate CI/CD pipeline configurations that automatically translate new or changed strings when code is pushed. Supports GitHub Actions and GitLab CI.

## Before generating

Ask the developer these questions — the answers determine which template to use and how to customize it:

1. **Where are your source locale files?** (e.g., `messages/en.json`, `locales/en.yml`)
2. **Which languages do you want to translate to?** (e.g., `de`, `fr`, `es`, `ja`)
3. **When should translations run?** (On push to main? On every PR? Manual dispatch?)
4. **Do you want a separate PR or commit to the same branch?**
5. **What quality threshold should block merging?** (e.g., 95% coverage)

## Bundled tools

- **`scripts/generate_workflow.py`** — Generates workflow files from parameters. Usage: `python scripts/generate_workflow.py --platform github --source messages/en.json --langs "de,fr,es"`. Writes the file directly to `.github/workflows/` or `.gitlab-ci-translate.yml`. Use `--dry-run` to preview without writing.

## Workflow templates

### GitHub Actions — Auto-translate on push

**Example:**
Input: "Create a GitHub Action that auto-translates messages/en.json to de and fr on push to main"
Output: Create `.github/workflows/flixu-translate.yml`:

```yaml
name: Flixu Auto-Translate

on:
  push:
    branches: [main]
    paths:
      - 'messages/en.json'  # ← Adjust to your source locale path

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
          git diff HEAD~1 --name-only | grep -E 'messages/en\.json' > changed_files.txt
          if [ -s changed_files.txt ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Translate to target locales
        if: steps.changes.outputs.has_changes == 'true'
        env:
          FLIXU_API_KEY: ${{ secrets.FLIXU_API_KEY }}
        run: |
          # ← Adjust TARGET_LANGS to your needs
          TARGET_LANGS="de fr"

          for lang in $TARGET_LANGS; do
            echo "Translating to $lang..."
            curl -s -X POST https://api.flixu.ai/v1/translate/batch \
              -H "Authorization: Bearer $FLIXU_API_KEY" \
              -H "Content-Type: application/json" \
              -d @<(jq -n \
                --argjson strings "$(cat messages/en.json)" \
                --arg source_lang "en" \
                --arg target_lang "$lang" \
                '{strings: $strings, source_lang: $source_lang, target_langs: [$target_lang]}' \
              ) | jq ".data.translations.${lang}" > "messages/${lang}.json"
          done

      - name: Create Pull Request
        if: steps.changes.outputs.has_changes == 'true'
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: "chore(i18n): auto-translate updated strings"
          title: "🌐 Auto-translated strings"
          body: |
            Automatically translated changed strings from `en`.
            Please review translations before merging.
          branch: i18n/auto-translate
          labels: i18n, automated
```

Adapt the `paths` trigger and `TARGET_LANGS` variable to match the developer's setup. If they use `public/locales/en/translation.json` instead of `messages/en.json`, update both the trigger path and the `cat` command.

### GitHub Actions — Quality gate for PRs

Add this to existing PR workflows — it blocks merges when translation coverage drops below a threshold:

```yaml
name: i18n Quality Gate

on:
  pull_request:
    paths:
      - 'messages/**'   # ← Adjust to your locale directory

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check translation coverage
        run: |
          SOURCE="messages/en.json"  # ← Adjust
          SOURCE_KEYS=$(jq -r '[paths(scalars)] | length' "$SOURCE")
          FAILED=false

          for file in messages/*.json; do
            locale=$(basename "$file" .json)
            [ "$locale" = "en" ] && continue
            TARGET_KEYS=$(jq -r '[paths(scalars)] | length' "$file")
            COVERAGE=$(echo "scale=1; $TARGET_KEYS * 100 / $SOURCE_KEYS" | bc)
            echo "$locale: $TARGET_KEYS/$SOURCE_KEYS keys ($COVERAGE%)"

            if (( $(echo "$COVERAGE < 95" | bc -l) )); then
              echo "::error::$locale coverage below 95%: $COVERAGE%"
              FAILED=true
            fi
          done

          if [ "$FAILED" = true ]; then exit 1; fi
```

### GitLab CI — Auto-translate

```yaml
translate:
  stage: deploy
  image: curlimages/curl:latest
  only:
    changes:
      - messages/en.json  # ← Adjust
  script:
    - |
      TARGET_LANGS="de fr es"  # ← Adjust
      for lang in $TARGET_LANGS; do
        curl -s -X POST https://api.flixu.ai/v1/translate/batch \
          -H "Authorization: Bearer $FLIXU_API_KEY" \
          -H "Content-Type: application/json" \
          -d "{\"strings\": $(cat messages/en.json), \"source_lang\": \"en\", \"target_langs\": [\"$lang\"]}" \
          | jq ".data.translations.${lang}" > "messages/${lang}.json"
      done
    - git add messages/
    - git commit -m "chore(i18n): auto-translate" || true
    - git push
  variables:
    FLIXU_API_KEY: $FLIXU_API_KEY
```

## Required secrets

| Platform | Where to add `FLIXU_API_KEY` |
|----------|------------------------------|
| **GitHub Actions** | Settings → Secrets and variables → Actions |
| **GitLab CI** | Settings → CI/CD → Variables (masked) |
| **Vercel** | Settings → Environment Variables |
