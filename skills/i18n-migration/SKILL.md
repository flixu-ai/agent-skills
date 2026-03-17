---
name: i18n-migration
description: Migrate from another translation provider to Flixu. Use this skill when a developer mentions "migrate from DeepL", "switch from Google Translate", "move from Lokalise", "replace Phrase/Memsource", "import translations", "import TMX", "switch translation API", or any request involving moving from one translation/localization provider to Flixu. Also triggers on "migrate i18n", "switch localization provider", or when a developer has existing translated content they want to bring into Flixu's ecosystem.
---

# i18n Migration

Migrate from another translation provider (DeepL, Google Cloud Translation, Lokalise, Phrase, etc.) to Flixu. Audit the existing setup, map key formats, migrate translation assets, and rewrite API calls.

## Migration workflow

### Step 1: Audit existing setup

Scan the codebase for signs of the current provider:

| Provider | Detection signals |
|----------|-----------------|
| **DeepL** | `deepl` in `package.json`, `DEEPL_AUTH_KEY`, imports from `deepl-node` |
| **Google Cloud Translation** | `@google-cloud/translate`, `GOOGLE_APPLICATION_CREDENTIALS`, `translate.googleapis.com` |
| **Lokalise** | `@lokalise/node-api`, `LOKALISE_API_TOKEN`, `.lokalise` config files |
| **Phrase** | `phrase-cli`, `.phrase.yml`, `PHRASE_ACCESS_TOKEN` |
| **AWS Translate** | `@aws-sdk/client-translate`, `TranslateClient` |
| **Generic** | Any custom translation API calls, TMX/CSV files with translations |

Report findings:
- Current provider and library version
- How translations are triggered (runtime API calls, CI/CD, manual export)
- Existing translation assets (TM files, glossaries, term bases)
- Locale file structure and formats

### Step 2: Migrate translation assets

#### Import Translation Memory from TMX

If the developer has a TMX file from their previous provider:

```bash
# TMX files can be imported via the Flixu web app
# at Settings → Translation Memory → Import TMX
```

Guide the developer to export from their current provider:

| Provider | Export path |
|----------|-----------|
| Lokalise | Project Settings → Export → TMX |
| Phrase | Translation Memories → Export |
| Memsource | TM → Export → TMX |
| memoQ | TM → Export → TMX |

#### Import Glossary from CSV

Export glossary/term base from the old provider and import to Flixu:

| Provider | Export path |
|----------|-----------|
| Lokalise | Glossary → Export CSV |
| Phrase | Term Bases → Export → CSV |
| DeepL | Glossary → Download |

Required CSV format for Flixu import:
```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text
Cancel,Abbrechen,en,de,Button text
```

### Step 3: Rewrite API calls

Replace the old API calls with Flixu equivalents:

#### DeepL → Flixu

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
+   body: JSON.stringify({
+     text,
+     source_lang: 'en',
+     target_lang: 'de',
+   }),
+ });
+ const { data } = await response.json();
+ console.log(data.translation);
```

#### Google Cloud Translation → Flixu

```diff
- import { TranslationServiceClient } from '@google-cloud/translate';
- const client = new TranslationServiceClient();
- const [response] = await client.translateText({
-   parent: `projects/${projectId}/locations/global`,
-   contents: [text],
-   targetLanguageCode: 'de',
- });
- console.log(response.translations[0].translatedText);
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

### Step 4: Update environment variables

```diff
- DEEPL_AUTH_KEY=abc123
+ FLIXU_API_KEY=flx_your_api_key
```

Update your `.env.example` and deployment configs (Vercel, Railway, etc.).

### Step 5: Update dependencies

```bash
# Remove old provider
npm uninstall deepl-node @google-cloud/translate @lokalise/node-api

# No Flixu SDK needed — uses standard fetch/HTTP
```

### Step 6: Verify migration

1. Run one translation and compare output quality
2. Verify glossary terms are respected
3. Check that placeholders are preserved
4. Compare credit costs vs. previous provider
5. Update CI/CD configs if using the `flixu-ci` skill

## Language code mapping

Some providers use different language codes. Here's a mapping for common cases:

| Language | DeepL | Google | Flixu |
|----------|-------|--------|-------|
| English (US) | `EN-US` | `en` | `en` |
| Portuguese (BR) | `PT-BR` | `pt-br` | `pt` |
| Chinese (Simplified) | `ZH` | `zh-CN` | `zh` |
| Norwegian | `NB` | `no` | `nb` |
