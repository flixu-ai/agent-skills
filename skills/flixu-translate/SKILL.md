---
name: flixu-translate
description: Translate text, i18n files, and documents using the Flixu API. Use this skill whenever a developer asks to "translate", "localize", "convert to German/French/Spanish", "translate this file", "translate my i18n keys", "localize my strings", "batch translate", or wants to translate any content — text, JSON, YAML, PO, XLIFF, DOCX, or other files — to another language. Also triggers on "flixu translate", "run translation", or any request involving converting content between natural languages. Even if the developer just says "make this work in German" or "we need a Spanish version", use this skill.
---

# Flixu Translate

Full translation workflow using the Flixu API. Detects file format, selects the correct endpoint, manages translation context, and writes output files to the correct locale directories.

## Prerequisites

- `FLIXU_API_KEY` environment variable set (or ask the developer for their key)
- The API key needs the `translate` scope

## Workflow

### Step 1: Determine what to translate

Detect the input type — this determines which API endpoint to use, because each endpoint is optimized for different content sizes and structures:

| Input type | How to detect | Endpoint | Why this one |
|-----------|---------------|----------|-------------|
| Inline text / string | No file path, raw text in prompt | `POST /v1/translate` | Lowest latency for short content |
| JSON/YAML i18n file | `.json`, `.yaml`, `.yml` with key-value structure | `POST /v1/translate/batch` | Preserves key structure, handles multiple target langs in one call |
| PO/POT file | `.po`, `.pot` with msgid/msgstr | `POST /v1/translate/document` | Preserves format-specific constructs (plural forms, contexts) |
| XLIFF/XLF | `.xliff`, `.xlf` | `POST /v1/translate/document` | Maintains translation units and metadata |
| DOCX/TXT/HTML/SRT | `.docx`, `.txt`, `.html`, `.srt`, `.vtt` | `POST /v1/translate/document` | Full document reconstruction in original format |
| iOS .strings | `.strings` | `POST /v1/translate/document` | Preserves key-value pair format |

### Step 2: Detect source and target languages

- If the developer specifies languages, use those
- If the source language is unclear, analyze the content or ask
- ISO 639-1 codes: `en`, `de`, `fr`, `es`, `zh`, `ja`, `ko`, `ar`, `pt`, `ru`, etc.

### Step 3: Execute translation

**Example 1 — single text:**
Input: "translate 'Welcome to our platform' to German"
Output:
```bash
curl -X POST https://api.flixu.ai/v1/translate \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Welcome to our platform", "source_lang": "en", "target_lang": "de"}'
```
→ Response: `{ "data": { "translation": "Willkommen auf unserer Plattform", "quality_score": 96 }, "meta": { ... } }`

**Example 2 — batch i18n file:**
Input: "translate my en.json to German and French"
Output: Read `en.json`, extract key-value pairs, call:
```bash
curl -X POST https://api.flixu.ai/v1/translate/batch \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"strings": {"greeting": "Hello", "farewell": "Goodbye"}, "source_lang": "en", "target_langs": ["de", "fr"]}'
```
→ Response: `{ "data": { "translations": { "de": { "greeting": "Hallo", ... }, "fr": { ... } } } }`

**Example 3 — document file:**
Input: "translate this XLIFF file to Japanese"
Output:
```bash
curl -X POST https://api.flixu.ai/v1/translate/document \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -F "file=@path/to/file.xliff" \
  -F "source_lang=en" \
  -F "target_lang=ja"
```
→ Response includes `file_data` (base64) — decode and write to disk.

### Step 4: Write output files

Write the output to the correct locale directory based on the framework:

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
- Credits used (from `meta.credits_used`)
- File paths written
- Any warnings (e.g., untranslated placeholders)

## Translation context

If the developer's organization has translation assets (glossaries, TMs, brand voices), including them significantly improves consistency — the AI uses glossary terms exactly and reuses approved TM matches:

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

To find available assets, use the `flixu-assets` skill or call `GET /v1/quota`.

## Error handling

| Status | Action |
|--------|--------|
| `402` | Insufficient credits — tell the developer to top up at app.flixu.ai/settings/billing |
| `429` | Rate limited — wait the number of seconds in `X-RateLimit-Reset` header, then retry |
| `400` | Invalid input — double-check language codes (ISO 639-1) and ensure the file format is supported |
