---
name: translation-qa
description: Audit translation quality and find localization issues in your codebase. Use this skill when a developer asks to "check translations", "find missing translations", "audit i18n", "validate locale files", "find untranslated strings", "check i18n quality", "scan for localization issues", "find duplicate translation keys", "validate interpolations", or any request involving checking the completeness, consistency, or quality of translations in a project. Also triggers on "translation coverage", "i18n audit", "missing keys", "locale sync", or even just "are my translations complete?". If a developer seems worried about translation quality or consistency, this skill helps.
---

# Translation QA

Scan a codebase for localization issues: missing translations, duplicate keys, inconsistent interpolations, hardcoded strings, and translation quality problems. Produce a structured report with actionable fix suggestions.

## Audit workflow

### Step 1: Detect i18n setup

Identify the framework and locale file structure — different frameworks store translations in different locations and formats:

| Framework | Locale files location | Key format |
|-----------|---------------------|------------|
| Next.js (next-intl) | `messages/*.json` | Nested JSON |
| React (react-i18next) | `public/locales/*/translation.json` | Nested JSON |
| Flutter | `lib/l10n/app_*.arb` | Flat JSON with `@` metadata |
| Rails | `config/locales/*.yml` | Nested YAML |
| iOS | `*.lproj/Localizable.strings` | Key-value pairs |
| Android | `values-*/strings.xml` | XML resources |

### Step 2: Run completeness check

Compare the source locale with all target locales. Missing keys are the #1 cause of untranslated strings showing up in production:

1. Load source locale (e.g., `en.json`) — flatten to extract all leaf keys
2. Load each target locale — flatten same way
3. Find missing keys (source has, target doesn't)
4. Find extra keys (target has, source doesn't — potentially orphaned)
5. Calculate coverage: `(target keys / source keys) × 100%`

**Output format — always use this template:**
```
Translation Coverage Report
===========================
Source: en (423 keys)

| Locale | Keys | Missing | Extra | Coverage |
|--------|------|---------|-------|----------|
| de     | 418  | 5       | 0     | 98.8%    |
| fr     | 401  | 22      | 0     | 94.8%    |
| es     | 423  | 0       | 0     | 100%     |

Missing keys in 'de':
  - settings.notifications.email_digest
  - settings.notifications.push_enabled
  - errors.payment.card_declined
```

### Step 3: Validate interpolations

Check that dynamic variables are consistent across locales — a `{name}` in the source that becomes `{nom}` in the translation will cause a runtime crash:

**Example:**
Input: `en.json` has `"greeting": "Hello, {name}!"`, `de.json` has `"greeting": "Hallo, {nom}!"`
Output:
```
⚠ Mismatch in 'de':
  Key: greeting
  en: "Hello, {name}!"
  de: "Hallo, {nom}!"        ← '{nom}' should be '{name}'
```

Variable patterns to check:
- `{name}` — ICU MessageFormat
- `{{name}}` — Handlebars/Angular
- `%{name}` — Ruby/Rails
- `%s`, `%d` — C-style printf
- `${name}` — JavaScript template literals

### Step 4: Find hardcoded strings

Scan source files for user-facing strings that bypass the i18n system. These are invisible to translators and will never be localized:

Patterns to flag:
- String literals in JSX: `<h1>Welcome</h1>` → should be `<h1>{t('welcome')}</h1>`
- `placeholder="Search..."` → should use translation function
- `title="Settings"` → should use translation function
- Alert/confirm messages: `alert("Are you sure?")` → should use translation

Exclusions (don't flag these — they're intentionally not translated):
- CSS class names, HTML attributes (`className`, `id`, `href`)
- Console.log messages (developer-only)
- Error codes and technical identifiers
- Single-character strings and numbers
- Strings in test files

**Output format:**
```
Hardcoded Strings Found
=======================
⚠ src/components/Header.tsx:15
  <h1>Welcome back</h1>
  Suggestion: <h1>{t('header.welcome_back')}</h1>

Found 12 hardcoded strings across 7 files.
```

### Step 5: Quality analysis (optional, requires FLIXU_API_KEY)

If the developer has a Flixu API key, sample 10-20 translations and run quality analysis:

```bash
curl -X POST https://api.flixu.ai/v1/analyze/headless \
  -H "Authorization: Bearer $FLIXU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "THE_TRANSLATED_TEXT", "source_lang": "en", "target_lang": "de"}'
```

This returns quality scores and risk signals without consuming translation credits.

### Step 6: Generate summary report

**Always end with this structured summary:**
```markdown
# i18n Audit Report

## Summary
- **Source locale**: en (423 keys)
- **Target locales**: de, fr, es
- **Overall coverage**: 96.5%
- **Interpolation issues**: 3
- **Hardcoded strings**: 12
- **Quality score avg**: 91/100

## Action Items (priority order)
1. Fix 3 interpolation mismatches (these cause runtime crashes)
2. Add 22 missing keys to `fr.json`
3. Extract 12 hardcoded strings to locale files
```

## Automated fixes

For missing keys, suggest using the `flixu-translate` skill:
```
"Translate the 22 missing keys from en to French"
```

For hardcoded strings, generate code diffs that extract strings to the locale file and replace them with `t()` calls.
