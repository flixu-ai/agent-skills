---
name: flixu-ci
description: Generate CI/CD pipeline configurations that automate translation on every push. Use this skill when a developer asks to "automate translations", "add translation to CI", "create GitHub Action for translation", "create GitLab CI for i18n", "auto-translate on push", "translation pipeline", "localization workflow automation", or any request involving automating the translation of locale files as part of a CI/CD workflow. Also triggers on "translation PR", "auto-localize", or "continuous localization".
---

# Flixu CI

Generate CI/CD pipeline configurations that automatically translate new or changed strings when code is pushed.

## Workflow templates

### GitHub Actions — Auto-translate on push

Create `.github/workflows/flixu-translate.yml`:

```yaml
name: Flixu Auto-Translate

on:
  push:
    branches: [main, develop]
    paths:
      - 'messages/en.json'
      - 'public/locales/en/**'
      - 'locales/en.yml'

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
          # Compare source locale with previous commit
          git diff HEAD~1 --name-only | grep -E '(messages/en\.json|locales/en|en\.ya?ml)' > changed_files.txt
          if [ -s changed_files.txt ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          else
            echo "has_changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Translate changed files
        if: steps.changes.outputs.has_changes == 'true'
        env:
          FLIXU_API_KEY: ${{ secrets.FLIXU_API_KEY }}
        run: |
          # Read source locale and translate to all targets
          TARGET_LANGS="de fr es ja"

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
            Automatically translated changed strings from `en` to target locales.

            **Translated to**: de, fr, es, ja
            **Trigger**: Push to `${{ github.ref_name }}`

            Please review translations before merging.
          branch: i18n/auto-translate
          labels: i18n, automated
```

### GitHub Actions — Translation quality gate

Add to your existing PR workflow in `.github/workflows/i18n-quality.yml`:

```yaml
name: i18n Quality Gate

on:
  pull_request:
    paths:
      - 'messages/**'
      - 'locales/**'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check translation coverage
        run: |
          SOURCE="messages/en.json"
          SOURCE_KEYS=$(jq -r '[paths(scalars)] | length' "$SOURCE")

          for file in messages/*.json; do
            locale=$(basename "$file" .json)
            [ "$locale" = "en" ] && continue
            TARGET_KEYS=$(jq -r '[paths(scalars)] | length' "$file")
            COVERAGE=$(echo "scale=1; $TARGET_KEYS * 100 / $SOURCE_KEYS" | bc)
            echo "$locale: $TARGET_KEYS/$SOURCE_KEYS keys ($COVERAGE%)"

            if (( $(echo "$COVERAGE < 95" | bc -l) )); then
              echo "::error::$locale coverage below 95%: $COVERAGE%"
              exit 1
            fi
          done

      - name: Validate interpolations
        run: |
          # Check that all {variables} in source exist in translations
          SOURCE="messages/en.json"
          for file in messages/*.json; do
            locale=$(basename "$file" .json)
            [ "$locale" = "en" ] && continue

            jq -r 'paths(scalars) as $p | "\($p | join("."))\t\(getpath($p))"' "$SOURCE" | while IFS=$'\t' read -r key value; do
              source_vars=$(echo "$value" | grep -oP '\{[^}]+\}' | sort)
              target_value=$(jq -r "getpath($(echo "$key" | jq -R 'split(".")'))" "$file" 2>/dev/null)
              target_vars=$(echo "$target_value" | grep -oP '\{[^}]+\}' | sort)

              if [ "$source_vars" != "$target_vars" ] && [ -n "$source_vars" ]; then
                echo "::warning::$locale/$key: variable mismatch (source: $source_vars, target: $target_vars)"
              fi
            done
          done
```

### GitLab CI — Auto-translate

Create `.gitlab-ci.yml` translation stage:

```yaml
translate:
  stage: deploy
  image: curlimages/curl:latest
  only:
    changes:
      - messages/en.json
  script:
    - |
      TARGET_LANGS="de fr es"
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

The developer needs to add the Flixu API key as a CI/CD secret:

| Platform | Secret location |
|----------|----------------|
| **GitHub Actions** | Settings → Secrets → Actions → `FLIXU_API_KEY` |
| **GitLab CI** | Settings → CI/CD → Variables → `FLIXU_API_KEY` |
| **Vercel** | Settings → Environment Variables → `FLIXU_API_KEY` |

## Customization points

Ask the developer:
1. **Source locale file path** — where is `en.json` or equivalent?
2. **Target languages** — which locales to translate to?
3. **Trigger** — on push to main? On every PR? Manual dispatch?
4. **Quality threshold** — minimum coverage % to pass the gate?
5. **PR strategy** — create separate PR or push to same branch?
