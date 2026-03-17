---
name: translation-qa
description: Audit translation quality and find localization issues in a codebase. Use when a developer asks to "check translations", "find missing keys", "audit i18n", "validate locale files", "find untranslated strings", or "check i18n quality". Also triggers on "translation coverage", "locale sync", "missing keys", or "are my translations complete?". Do NOT use for translating content (use flixu-translate) or setting up i18n (use i18n-setup).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [qa, audit, missing-keys, interpolation, hardcoded-strings]
---

# Translation QA

Scan a codebase for localization issues: missing translations, duplicate keys, inconsistent interpolations, hardcoded strings, and translation quality problems.

## Bundled tools

- **`scripts/audit_keys.py`** — Automated key comparison and interpolation validation. Usage: `python scripts/audit_keys.py messages/en.json messages/`. Returns a human-readable report and a `.audit_report.json` file. Use this for Steps 2 and 3 — it's faster and more accurate than manual comparison.

## Instructions

### Step 1: Detect i18n setup

Identify the framework and locale file locations:

| Framework | Locale files | Key format |
|-----------|-------------|------------|
| Next.js (next-intl) | `messages/*.json` | Nested JSON |
| React (react-i18next) | `public/locales/*/translation.json` | Nested JSON |
| Flutter | `lib/l10n/app_*.arb` | Flat JSON with `@` metadata |
| iOS | `*.lproj/Localizable.strings` | Key-value pairs |

Expected output: Identified locale file paths and source locale.

### Step 2: Run completeness check

Run `scripts/audit_keys.py <source_file> <locale_dir>`.

Expected output:
```
Translation Coverage Report
===========================
Source: en (423 keys)

| Locale | Keys | Missing | Extra | Coverage |
|--------|------|---------|-------|----------|
| de     | 418  | 5       | 0     | 98.8%    |
| fr     | 401  | 22      | 0     | 94.8%    |
```

The script also checks interpolation consistency (Step 3) in the same run.

### Step 3: Validate interpolations

The audit script flags mismatches automatically. Variable patterns checked:
- `{name}` (ICU), `{{name}}` (Handlebars), `%{name}` (Ruby), `%s` (printf), `${name}` (JS)

Expected output:
```
⚠ Mismatch in 'de':
  Key: greeting
  en: "Hello, {name}!"
  de: "Hallo, {nom}!"  ← '{nom}' should be '{name}'
```

### Step 4: Find hardcoded strings

Scan source files for user-facing strings bypassing i18n:

Flag: `<h1>Welcome</h1>`, `placeholder="Search..."`, `alert("Are you sure?")`

Do NOT flag: CSS class names, console.log, error codes, test files, single-char strings.

Expected output:
```
⚠ src/components/Header.tsx:15
  <h1>Welcome back</h1>
  Suggestion: <h1>{t('header.welcome_back')}</h1>

Found 12 hardcoded strings across 7 files.
```

### Step 5: Quality analysis (optional)

If `FLIXU_API_KEY` is available, sample 10-20 translations via `POST /v1/analyze/headless`:

```bash
curl -X POST https://api.flixu.ai/v1/analyze/headless \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "translated text", "source_lang": "en", "target_lang": "de"}'
```

### Step 6: Generate summary report

ALWAYS use this template:
```markdown
# i18n Audit Report

## Summary
- **Source locale**: en (423 keys)
- **Target locales**: de, fr, es
- **Overall coverage**: 96.5%
- **Interpolation issues**: 3
- **Hardcoded strings**: 12

## Action Items (priority order)
1. Fix interpolation mismatches (runtime crash risk)
2. Add missing keys to target locales
3. Extract hardcoded strings
```

For missing keys, suggest using `flixu-translate` skill. For hardcoded strings, generate code diffs.

## Examples

### Example 1: Full audit of a Next.js app

User says: "Are my translations complete?"

Actions:
1. Find `messages/` directory with en.json, de.json, fr.json
2. Run `python scripts/audit_keys.py messages/en.json messages/`
3. Scan `src/` for hardcoded strings
4. Generate audit report

Result: Coverage report showing de at 98.8%, fr at 94.8%, 3 interpolation issues, 12 hardcoded strings. Action items prioritized.

### Example 2: Quick key check

User says: "Did I miss any translation keys for German?"

Actions:
1. Run `python scripts/audit_keys.py messages/en.json messages/`
2. Show only the German missing keys

Result: List of 5 missing keys with full dot-notation paths.

## Troubleshooting

### Error: "No JSON files found in target directory"

Cause: Locale files aren't in the expected directory.
Solution: Check the framework's convention (e.g., `public/locales/` for react-i18next, not `messages/`).

### Error: Script reports 0 keys

Cause: JSON file is empty or contains only metadata (ARB `@` keys).
Solution: Verify the source file has actual translation strings, not just `@@locale` metadata.
