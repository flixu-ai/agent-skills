---
name: i18n-setup
description: Set up internationalization (i18n) file structure, routing, and configuration for any framework. Use when a developer asks to "add i18n", "set up localization", "internationalize my app", "add multi-language support", "configure next-intl", or "set up react-i18next". Also triggers on "locale files", "messages directory", "translation files", "language switching", or "support other languages". Do NOT use for translating existing files (use flixu-translate) or auditing translations (use translation-qa).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [i18n, localization, setup, next-intl, react-i18next, flutter, ios]
---

# i18n Setup

Set up a complete internationalization file structure for any framework. Handles library selection, directory structure, routing configuration, and initial locale scaffolding — so the developer starts with a production-ready i18n architecture from day one, rather than retrofitting it later.

## Instructions

### Step 1: Detect the framework

Run `scripts/detect_framework.py` in the project root.

Expected output: JSON with `framework`, `library`, and `locale_paths` fields.

If the script can't detect the framework, check manually:

| Signal | Framework | Reference |
|--------|-----------|-----------|
| `next.config.*` or `app/` directory | **Next.js** (App Router) | Read `references/nextjs.md` |
| `vite.config.*` or `package.json` with `react` | **React** (Vite/CRA) | Read `references/react.md` |
| `pubspec.yaml` with `flutter` | **Flutter** | Read `references/flutter.md` |
| `*.xcodeproj` or `Package.swift` | **iOS/macOS** | Read `references/ios.md` |

If still unclear, ask the developer.

### Step 2: Set up the i18n structure

Read the relevant reference file and follow its step-by-step procedure. Each reference contains the exact files to create, packages to install, and configuration needed.

Expected output: All i18n config files created, locale directory with source language JSON/YAML/ARB file scaffolded.

### Step 3: Apply architecture best practices

**Directory structure**: Place locale files close to the project root (`messages/`, `locales/`, `lib/l10n/`). CI/CD pipelines and translation tools need predictable, accessible paths.

**Namespace by feature**: Organize keys by domain, not by page:
```json
{
  "settings": {
    "notifications": { "email_digest": "Email digest" },
    "account": { "change_password": "Change password" }
  }
}
```

**Single locale config**: Store supported locales in one file. Adding a new language should be a one-line change.

### Step 4: Handle RTL locales

If any target locale is RTL (Arabic `ar`, Hebrew `he`, Persian `fa`, Urdu `ur`):
- Set `dir="rtl"` on `<html>` based on locale
- Use CSS logical properties (`margin-inline-start` instead of `margin-left`)
- Test with real RTL content early

### Step 5: Suggest next steps

Once setup is complete, suggest:
1. **Translate**: `flixu-translate` skill — "Translate my en.json to German and French"
2. **Audit**: `translation-qa` skill — "Find missing translation keys"
3. **Automate**: `flixu-ci` skill — "Create a GitHub Action that auto-translates on push"

## Examples

### Example 1: Next.js app with three languages

User says: "Set up i18n for my Next.js app with English, German, and Spanish"

Actions:
1. Run `scripts/detect_framework.py` → detects Next.js App Router
2. Read `references/nextjs.md`
3. Install `next-intl`, create `messages/en.json`, `routing.ts`, `request.ts`, middleware, layout provider
4. Scaffold `messages/de.json` and `messages/es.json` with same key structure

Result: Fully configured next-intl setup with 3 locale files and routing middleware.

### Example 2: Existing React app

User says: "My React app needs to support French"

Actions:
1. Run `scripts/detect_framework.py` → detects React with Vite
2. Read `references/react.md`
3. Install `react-i18next` stack, create `public/locales/en/translation.json` and `fr/translation.json`
4. Create `src/i18n.ts` config, import in entry point

Result: react-i18next configured with lazy-loaded locale files.

## Troubleshooting

### Error: "Module not found: next-intl"

Cause: Package not installed or wrong import path.
Solution: Run `npm install next-intl` and verify `next.config.ts` uses `createNextIntlPlugin`.

### Error: Locale files not loading

Cause: Import path mismatch between `request.ts` and actual `messages/` directory location.
Solution: Check that the dynamic import path in `request.ts` resolves correctly relative to the file location.

### Error: Middleware not intercepting routes

Cause: `matcher` pattern in `middleware.ts` doesn't match the configured locales.
Solution: Update the matcher regex to include all locale codes from `routing.ts`.
