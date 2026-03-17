---
name: flixu-translate
description: Translate text, JSON, YAML, XLIFF, PO, DOCX, and other files using the Flixu API. Use when a developer asks to "translate", "localize", "convert to German", "translate this file", "batch translate", or wants content in another language. Also triggers on "flixu translate", "run translation", or "make this work in Spanish". Do NOT use for setting up i18n architecture (use i18n-setup) or auditing existing translations (use translation-qa).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [translation, localization, api, batch, document]
---

# Flixu Translate

Full translation workflow using the Flixu API. Detects file format, selects the correct endpoint, manages translation context, and writes output files to the correct locale directories.

## Prerequisites

- `FLIXU_API_KEY` environment variable set
- API key needs the `translate` scope

## Bundled tools

- **`scripts/translate.py`** — Translates JSON locale files directly. Usage: `python scripts/translate.py messages/en.json "de,fr,es"`. Handles nested JSON flattening/unflattening automatically.
- **`references/formats.md`** — Details on what each file format preserves (XLIFF metadata, PO plurals, SRT timestamps).

## Instructions

### Step 1: Determine what to translate

| Input type | Detection | Endpoint |
|-----------|-----------|----------|
| Inline text | No file path, raw text | `POST /v1/translate` |
| JSON/YAML i18n file | `.json`, `.yaml` with key-value structure | `POST /v1/translate/batch` |
| PO/XLIFF/.strings/DOCX/SRT | Structured document formats | `POST /v1/translate/document` |

For format-specific details, read `references/formats.md`.

Expected output: Identified input type and target endpoint.

### Step 2: Detect languages

- Use developer-specified languages if provided
- ISO 639-1 codes: `en`, `de`, `fr`, `es`, `zh`, `ja`, `ko`, `ar`, `pt`, `ru`
- If source language is unclear, analyze content or ask

### Step 3: Execute translation

**Text** (`POST /v1/translate`):
```bash
curl -X POST https://api.flixu.ai/v1/translate \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Welcome", "source_lang": "en", "target_lang": "de"}'
```

Expected output: `{ "data": { "translation": "Willkommen", "quality_score": 96 }, "meta": { ... } }`

**Batch** (`POST /v1/translate/batch`):
```bash
curl -X POST https://api.flixu.ai/v1/translate/batch \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"strings": {"greeting": "Hello"}, "source_lang": "en", "target_langs": ["de", "fr"]}'
```

Expected output: `{ "data": { "translations": { "de": { "greeting": "Hallo" }, "fr": { ... } } } }`

For JSON locale files, prefer running `scripts/translate.py` — it handles flattening, API calls, and file writing in one step.

**Document** (`POST /v1/translate/document`):
```bash
curl -X POST https://api.flixu.ai/v1/translate/document \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -F "file=@path/to/file.xliff" \
  -F "source_lang=en" \
  -F "target_lang=ja"
```

Expected output: Response with `file_data` (base64) to decode and write.

### Step 4: Write output files

| Framework | Output path |
|-----------|-------------|
| Next.js (next-intl) | `messages/{locale}.json` |
| React (react-i18next) | `public/locales/{locale}/translation.json` |
| Flutter | `lib/l10n/app_{locale}.arb` |
| iOS | `{locale}.lproj/Localizable.strings` |

Reconstruct nested JSON if the source used nested keys.

### Step 5: Report results

Report: strings/chars translated, quality scores, credits used (`meta.credits_used`), file paths written, warnings.

### Optional: Translation context

Include glossary/TM/brand voice for better consistency:
```json
{
  "glossary_ids": ["gloss_abc"],
  "tm_id": "tm_def",
  "brand_voice_id": "bv_ghi"
}
```

## Examples

### Example 1: Translate a JSON locale file

User says: "Translate my en.json to German and French"

Actions:
1. Run `python scripts/translate.py messages/en.json "de,fr"`
2. Script reads en.json, calls batch API, writes messages/de.json and messages/fr.json

Result: Two new locale files with all keys translated, nested structure preserved.

### Example 2: Translate inline text

User says: "How do you say 'Your subscription has been renewed' in Japanese?"

Actions:
1. Call `POST /v1/translate` with source text
2. Return translation with quality score

Result: `"サブスクリプションが更新されました"` (quality_score: 94)

## Troubleshooting

### Error: 402 Payment Required

Cause: Insufficient credits in the organization's account.
Solution: Tell the developer to top up at app.flixu.ai/settings/billing.

### Error: 429 Too Many Requests

Cause: Plan rate limit exceeded.
Solution: Wait the number of seconds in the `X-RateLimit-Reset` response header, then retry.

### Error: 400 Bad Request

Cause: Invalid language code or unsupported file format.
Solution: Verify language codes are ISO 639-1 and file format is in the supported list (see `references/formats.md`).
