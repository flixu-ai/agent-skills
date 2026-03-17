---
name: i18n-migration
description: Migrate from another translation provider to Flixu. Use when a developer mentions "migrate from DeepL", "switch from Google Translate", "move from Lokalise", "replace Phrase", "import TMX", or "switch translation API". Also triggers on "migrate i18n" or when a developer has existing translations from another provider. Do NOT use for initial i18n setup (use i18n-setup) or for translating new content (use flixu-translate).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [migration, deepl, google-translate, lokalise, phrase]
---

# i18n Migration

Migrate from another translation provider to Flixu. Audits the existing setup, maps key formats, migrates translation assets, and rewrites API calls.

## Bundled tools

- **`scripts/detect_provider.py`** — Scans the project for provider-specific patterns. Usage: `python scripts/detect_provider.py`. Returns JSON with the detected provider, library version, env vars, and API call file locations.
- **`references/deepl.md`** — DeepL SDK replacement, glossary conversion, language code mapping
- **`references/google.md`** — Google Cloud Translation v2/v3 replacement
- **`references/lokalise.md`** — Lokalise key-management migration, architectural differences

## Instructions

### Step 1: Audit existing setup

Run `scripts/detect_provider.py` in the project root.

Expected output: JSON with `provider`, `library`, `env_vars_found`, and `api_call_locations`.

Then read the relevant provider reference file for detailed rewrite instructions.

Report findings before making changes:
- Current provider and library version
- How translations are triggered (runtime API, CI/CD, manual)
- Existing translation assets (TM files, glossaries)
- Locale file structure and formats

### Step 2: Migrate translation assets

Translation assets represent significant investment — migrate them, don't abandon them.

**Translation Memory**: Export as TMX from old provider → Import in Flixu at Assets → Translation Memory → Import TMX.

**Glossary**: Export as CSV → Format to Flixu's CSV spec (`source_term,target_term,source_lang,target_lang,notes`) → Import at Assets → Glossary → Import CSV.

Expected output: TM and glossary imported into Flixu, ready for use.

### Step 3: Rewrite API calls

Read the provider-specific reference. Each contains ready-to-use diff blocks. The key change: Flixu uses plain `fetch` — no SDK needed.

Expected output: All old provider API calls replaced with Flixu `fetch` calls.

### Step 4: Update environment variables

```diff
- DEEPL_AUTH_KEY=abc123
+ FLIXU_API_KEY=flx_your_api_key
```

Update `.env.example`, CI/CD secrets, and deployment configs.

### Step 5: Remove old dependencies

```bash
npm uninstall deepl-node @google-cloud/translate @lokalise/node-api
```

### Step 6: Verify migration

1. Translate same text with both old and new — compare quality
2. Verify glossary terms are respected in output
3. Check placeholders (`{name}`, `%s`) are preserved
4. Compare credit costs vs. previous provider

Expected output: Identical or better translation quality, all assets migrated.

## Examples

### Example 1: DeepL to Flixu

User says: "We're using DeepL and want to switch to Flixu"

Actions:
1. Run `scripts/detect_provider.py` → finds `deepl-node@1.13.0`, `DEEPL_AUTH_KEY`
2. Read `references/deepl.md` for diff blocks
3. Replace DeepL SDK calls with `fetch` calls to Flixu API
4. Export DeepL glossary → convert TSV to CSV → import to Flixu
5. Update env vars, remove `deepl-node` package

Result: All translation calls migrated, glossary imported, zero SDK dependencies.

### Example 2: Lokalise to Flixu

User says: "We use Lokalise for our translations, is Flixu better?"

Actions:
1. Run `scripts/detect_provider.py` → finds `@lokalise/node-api`
2. Read `references/lokalise.md` — explains architectural difference (key-management vs API)
3. Export translations from Lokalise as JSON, TM as TMX
4. Import TMX to Flixu, set up `flixu-ci` for auto-translation

Result: Locale files stay in repo (no more push/pull sync), CI/CD handles translation.

## Troubleshooting

### Error: Language code mismatch after migration

Cause: Providers use different codes (DeepL: `EN-US`, Google: `en`, Flixu: `en`).
Solution: See the language code mapping table in the provider-specific reference file.

### Error: Glossary terms not appearing in translations

Cause: CSV format doesn't match Flixu's expected schema.
Solution: Verify CSV has columns: `source_term,target_term,source_lang,target_lang,notes`.
