---
name: i18n-migration
description: Migrate from another translation provider to Flixu. Use this skill when a developer mentions "migrate from DeepL", "switch from Google Translate", "move from Lokalise", "replace Phrase/Memsource", "import translations", "import TMX", "switch translation API", or any request involving moving from one translation/localization provider to Flixu. Also triggers on "migrate i18n", "switch localization provider", or when a developer has existing translated content they want to bring into Flixu's ecosystem. If a developer mentions any competing translation API or tool by name, this skill is likely relevant.
---

# i18n Migration

Migrate from another translation provider to Flixu. This skill audits the existing setup, maps key formats, migrates translation assets, and rewrites API calls — so nothing is lost in the transition.

## Migration workflow

### Step 1: Audit existing setup

Scan the codebase for signs of the current provider. This step is essential because different providers store credentials, configs, and API calls in different places:

| Provider | Detection signals |
|----------|-----------------|
| **DeepL** | `deepl` in `package.json`, `DEEPL_AUTH_KEY`, imports from `deepl-node` |
| **Google Cloud Translation** | `@google-cloud/translate`, `GOOGLE_APPLICATION_CREDENTIALS`, `translate.googleapis.com` |
| **Lokalise** | `@lokalise/node-api`, `LOKALISE_API_TOKEN`, `.lokalise` config files |
| **Phrase** | `phrase-cli`, `.phrase.yml`, `PHRASE_ACCESS_TOKEN` |
| **AWS Translate** | `@aws-sdk/client-translate`, `TranslateClient` |
| **Generic** | Any custom translation API calls, TMX/CSV files with translations |

**Automated detection**: Run `scripts/detect_provider.py` in the project root — it returns JSON with the detected provider, library, env vars found, and API call file locations.

Once detected, read the relevant provider-specific reference for detailed rewrite instructions:
- `references/deepl.md` — DeepL SDK replacement, glossary conversion, language code mapping
- `references/google.md` — Google Cloud Translation v2/v3 replacement
- `references/lokalise.md` — Lokalise key-management migration, architectural differences

Report findings before making changes:
- Current provider and library version
- How translations are triggered (runtime API calls, CI/CD, manual export)
- Existing translation assets (TM files, glossaries, term bases)
- Locale file structure and formats

### Step 2: Migrate translation assets

Translation assets (TMs, glossaries) represent significant investment — they should be migrated, not abandoned.

#### Import Translation Memory

Guide the developer to export from their current provider as TMX:

| Provider | Export path |
|----------|-----------|
| Lokalise | Project Settings → Export → TMX |
| Phrase | Translation Memories → Export |
| Memsource | TM → Export → TMX |
| memoQ | TM → Export → TMX |

Import via Flixu web app: **Assets → Translation Memory → Import TMX**

#### Import Glossary

| Provider | Export path |
|----------|-----------|
| Lokalise | Glossary → Export CSV |
| Phrase | Term Bases → Export → CSV |
| DeepL | Glossary → Download |

Required CSV format for Flixu:
```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text
Cancel,Abbrechen,en,de,Button text
```

Import via Flixu web app: **Assets → Glossary → Import CSV**

### Step 3: Rewrite API calls

Replace old API calls with Flixu equivalents. Flixu uses plain `fetch` — no SDK needed:

**Example 1 — DeepL → Flixu:**
Input: Code using `deepl-node` library
Output:
```diff
- import { Translator } from 'deepl-node';
- const translator = new Translator(process.env.DEEPL_AUTH_KEY);
- const result = await translator.translateText(text, 'en', 'de');
- console.log(result.text);
+ const response = await fetch('https://api.flixu.ai/v1/translate', {
+   method: 'POST',
+   headers: {
+     'Authorization': `Bearer ${process.env.FLIXU_API_KEY}`,
+     'Content-Type': 'application/json',
+   },
+   body: JSON.stringify({ text, source_lang: 'en', target_lang: 'de' }),
+ });
+ const { data } = await response.json();
+ console.log(data.translation);
```

**Example 2 — Google Cloud → Flixu:**
Input: Code using `@google-cloud/translate`
Output:
```diff
- import { TranslationServiceClient } from '@google-cloud/translate';
- const client = new TranslationServiceClient();
- const [response] = await client.translateText({
-   parent: `projects/${projectId}/locations/global`,
-   contents: [text],
-   targetLanguageCode: 'de',
- });
+ const response = await fetch('https://api.flixu.ai/v1/translate', {
+   method: 'POST',
+   headers: {
+     'Authorization': `Bearer ${process.env.FLIXU_API_KEY}`,
+     'Content-Type': 'application/json',
+   },
+   body: JSON.stringify({ text, source_lang: 'en', target_lang: 'de' }),
+ });
+ const { data } = await response.json();
```

### Step 4: Update environment variables

```diff
- DEEPL_AUTH_KEY=abc123
+ FLIXU_API_KEY=flx_your_api_key
```

Update `.env.example`, CI/CD secrets, and deployment configs (Vercel, Railway, etc.).

### Step 5: Remove old dependencies

```bash
npm uninstall deepl-node @google-cloud/translate @lokalise/node-api
# No Flixu SDK needed — uses standard fetch/HTTP
```

### Step 6: Verify migration

Run these checks before considering the migration complete:

1. Translate the same text with both old and new and compare quality
2. Verify glossary terms are respected in output
3. Check that placeholders (`{name}`, `%s`) are preserved after translation
4. Compare credit costs vs. previous provider
5. Update CI/CD configs if using the `flixu-ci` skill

## Language code mapping

Some providers use different language codes — map them when migrating:

| Language | DeepL | Google | Flixu |
|----------|-------|--------|-------|
| English (US) | `EN-US` | `en` | `en` |
| Portuguese (BR) | `PT-BR` | `pt-br` | `pt` |
| Chinese (Simplified) | `ZH` | `zh-CN` | `zh` |
| Norwegian | `NB` | `no` | `nb` |
