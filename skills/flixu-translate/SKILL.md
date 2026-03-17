---
name: flixu-translate
description: Translate text, i18n files, and documents using the Flixu API. Use this skill whenever a developer asks to "translate", "localize", "convert to German/French/Spanish", "translate this file", "translate my i18n keys", "localize my strings", "batch translate", or wants to translate any content — text, JSON, YAML, PO, XLIFF, DOCX, or other files — to another language. Also triggers on "flixu translate", "run translation", or any request involving converting content between natural languages.
---

# Flixu Translate

Full translation workflow using the Flixu API. Detects file format, selects the correct endpoint, manages translation context, and writes output files to the correct locale directories.

## Prerequisites

- `FLIXU_API_KEY` environment variable set (or ask the developer for their key)
- The API key needs the `translate` scope

## Workflow

### Step 1: Understand what to translate

Determine the input:

| Input type | How to detect | Endpoint |
|-----------|---------------|----------|
| Inline text / string | No file path, raw text in the prompt | `POST /v1/translate` |
| JSON/YAML i18n file | `.json`, `.yaml`, `.yml` with key-value structure | `POST /v1/translate/batch` |
| PO/POT file | `.po`, `.pot` with msgid/msgstr | `POST /v1/translate/document` |
| XLIFF/XLF | `.xliff`, `.xlf` | `POST /v1/translate/document` |
| DOCX/TXT/HTML/SRT | `.docx`, `.txt`, `.html`, `.srt`, `.vtt` | `POST /v1/translate/document` |
| iOS .strings | `.strings` | `POST /v1/translate/document` |

### Step 2: Detect source and target languages

- If the developer specifies languages, use those
- If the source language is unclear, analyze the content or ask
- ISO 639-1 codes: `en`, `de`, `fr`, `es`, `zh`, `ja`, `ko`, `ar`, `pt`, `ru`, etc.

### Step 3: Execute translation

#### Text translation (`POST /v1/translate`)

For single strings or short text:

```bash
curl -X POST https://api.flixu.ai/v1/translate \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "THE_TEXT_TO_TRANSLATE",
    "source_lang": "en",
    "target_lang": "de"
  }'
```

Response: `{ "data": { "translation": "...", "quality_score": 94 }, "meta": { ... } }`

#### Batch translation (`POST /v1/translate/batch`)

For i18n key-value files (JSON, YAML). Extract the strings as a key-value map:

```bash
curl -X POST https://api.flixu.ai/v1/translate/batch \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "strings": {
      "greeting": "Hello",
      "farewell": "Goodbye",
      "cta": "Sign up now"
    },
    "source_lang": "en",
    "target_langs": ["de", "fr"]
  }'
```

Response: `{ "data": { "translations": { "de": { "greeting": "Hallo", ... }, "fr": { ... } } } }`

#### Document translation (`POST /v1/translate/document`)

For structured files (XLIFF, PO, DOCX, SRT, .strings):

```bash
curl -X POST https://api.flixu.ai/v1/translate/document \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -F "file=@path/to/file.xliff" \
  -F "source_lang=en" \
  -F "target_lang=de"
```

Response includes `file_data` (base64) which you decode and write to disk.

### Step 4: Write output files

After translation, write the output to the correct locale directory:

| Framework | Output path pattern |
|-----------|-------------------|
| Next.js (next-intl) | `messages/{locale}.json` |
| React (react-i18next) | `public/locales/{locale}/translation.json` |
| Flutter | `lib/l10n/app_{locale}.arb` |
| Rails | `config/locales/{locale}.yml` |
| iOS | `{locale}.lproj/Localizable.strings` |
| Android | `app/src/main/res/values-{locale}/strings.xml` |
| Generic | `locales/{locale}.{ext}` |

For batch translations that return a flat key-value map, reconstruct the nested JSON structure if the source file used nested keys.

### Step 5: Report results

After writing files, report:
- Number of strings/characters translated
- Quality scores (if available)
- Credits used
- File paths written
- Any warnings (e.g., untranslated placeholders)

## Optional: Translation context

If the developer has Flixu assets (glossaries, TMs, brand voices), include them:

```json
{
  "text": "...",
  "source_lang": "en",
  "target_lang": "de",
  "glossary_ids": ["gloss_abc123"],
  "tm_id": "tm_def456",
  "brand_voice_id": "bv_ghi789"
}
```

To find available assets, use the `flixu-assets` skill or call `GET /v1/quota` to check the organization.

## Error handling

| Status | Action |
|--------|--------|
| `402` | Insufficient credits — tell the developer to top up at app.flixu.ai/settings/billing |
| `429` | Rate limited — wait `X-RateLimit-Reset` seconds and retry |
| `400` | Invalid input — check language codes and file format |
