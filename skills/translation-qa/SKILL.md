---
name: translation-qa
description: Audit translation quality and find localization issues in your codebase. Use this skill when a developer asks to "check translations", "find missing translations", "audit i18n", "validate locale files", "find untranslated strings", "check i18n quality", "scan for localization issues", "find duplicate translation keys", "validate interpolations", or any request involving checking the completeness, consistency, or quality of translations in a project. Also triggers on "translation coverage", "i18n audit", "missing keys", or "locale sync".
---

# Translation QA

Scan your codebase for localization issues: missing translations, duplicate keys, inconsistent interpolations, hardcoded strings, and translation quality problems.

## Audit workflow

### Step 1: Detect i18n setup

Identify the framework and locale file structure:

| Framework | Locale files location | Key format |
|-----------|---------------------|------------|
| Next.js (next-intl) | `messages/*.json` | Nested JSON |
| React (react-i18next) | `public/locales/*/translation.json` | Nested JSON |
| Flutter | `lib/l10n/app_*.arb` | Flat JSON with `@` metadata |
| Rails | `config/locales/*.yml` | Nested YAML |
| iOS | `*.lproj/Localizable.strings` | Key-value pairs |
| Android | `values-*/strings.xml` | XML resources |

### Step 2: Run completeness check

Compare the source locale with all target locales:

1. **Load source locale** (e.g., `en.json`) — extract all keys (flatten nested structures)
2. **Load each target locale** — extract all keys
3. **Find missing keys** — keys in source but not in target
4. **Find extra keys** — keys in target but not in source (potentially orphaned)
5. **Calculate coverage** — `(target keys / source keys) × 100%`

Report format:
```
Translation Coverage Report
===========================
Source: en (423 keys)

| Locale | Keys | Missing | Extra | Coverage |
|--------|------|---------|-------|----------|
| de     | 418  | 5       | 0     | 98.8%    |
| fr     | 401  | 22      | 0     | 94.8%    |
| es     | 423  | 0       | 0     | 100%     |
| ja     | 390  | 33      | 0     | 92.2%    |

Missing keys in 'de':
  - settings.notifications.email_digest
  - settings.notifications.push_enabled
  - errors.payment.card_declined
  - errors.payment.insufficient_funds
  - pricing.enterprise.custom_quote
```

### Step 3: Validate interpolations

Check that dynamic variables are consistent across locales:

```
Interpolation Consistency Check
================================
Source: en

⚠ Mismatch in 'de':
  Key: greeting
  en: "Hello, {name}!"
  de: "Hallo, {nom}!"        ← '{nom}' should be '{name}'

⚠ Missing variable in 'fr':
  Key: items_count
  en: "You have {count} items"
  fr: "Vous avez des articles"  ← '{count}' is missing

✓ All variables consistent in 'es' (423/423 keys)
```

Variable patterns to check:
- `{name}` — ICU MessageFormat
- `{{name}}` — Handlebars/Angular
- `%{name}` — Ruby/Rails
- `%s`, `%d` — C-style printf
- `${name}` — JavaScript template literals

### Step 4: Find hardcoded strings in components

Scan source files for user-facing strings that aren't using the i18n library:

Patterns to flag:
- String literals in JSX: `<h1>Welcome</h1>` → should be `<h1>{t('welcome')}</h1>`
- `placeholder="Search..."` → should use translation function
- `title="Settings"` → should use translation function
- Alert/confirm messages: `alert("Are you sure?")` → should use translation

Exclusions (don't flag):
- CSS class names, HTML attributes (`className`, `id`, `href`)
- Console.log messages
- Error codes and technical strings
- Single-character strings and numbers
- Strings in test files

Report as:
```
Hardcoded Strings Found
=======================
⚠ src/components/Header.tsx:15
  <h1>Welcome back</h1>
  Suggestion: <h1>{t('header.welcome_back')}</h1>

⚠ src/components/SearchBar.tsx:8
  placeholder="Search products..."
  Suggestion: placeholder={t('search.placeholder')}

Found 12 hardcoded strings across 7 files.
```

### Step 5: Quality analysis (optional, requires API key)

If the developer has a Flixu API key, run quality analysis on existing translations:

```bash
curl -X POST https://api.flixu.ai/v1/analyze/headless \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "THE_TRANSLATED_TEXT",
    "source_lang": "en",
    "target_lang": "de"
  }'
```

Report quality scores and risk signals for sampled translations.

### Step 6: Generate summary report

Compile all findings into a structured report:

```markdown
# i18n Audit Report

## Summary
- **Source locale**: en (423 keys)
- **Target locales**: de, fr, es, ja
- **Overall coverage**: 96.5%
- **Interpolation issues**: 3
- **Hardcoded strings**: 12
- **Quality score avg**: 91/100

## Action Items
1. Add 5 missing keys to `de.json`
2. Fix 3 interpolation mismatches
3. Extract 12 hardcoded strings to locale files
4. Translate 33 missing keys for `ja.json`
```

## Automated fix suggestions

For missing keys, suggest auto-generating them with the `flixu-translate` skill:

```
"Translate the 5 missing keys from en to de"
```

For hardcoded strings, generate the extraction as a code diff.
