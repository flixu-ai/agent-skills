# Lokalise → Flixu Migration

## Export translations from Lokalise

1. Go to your Lokalise project → **Download**
2. Choose **JSON** format (for key-value translations)
3. Download the ZIP containing locale files

Or export Translation Memory:
1. Go to **Translation Memory** → **Export** → **TMX**
2. Import the TMX file into Flixu: **Assets → Translation Memory → Import TMX**

## Export glossary

1. Go to **Glossary** → **Export** → **CSV**
2. Map the CSV columns to Flixu's format:
   ```csv
   source_term,target_term,source_lang,target_lang,notes
   ```

## API migration (if using Lokalise API)

```diff
- import { LokaliseApi } from '@lokalise/node-api';
- const lokalise = new LokaliseApi({ apiKey: process.env.LOKALISE_API_TOKEN });
- const keys = await lokalise.keys().list({
-   project_id: PROJECT_ID,
-   filter_translation_lang_ids: 'de',
- });
+ // Flixu doesn't use a project-key model
+ // Instead, send source text directly for translation:
+ const response = await fetch('https://api.flixu.ai/v1/translate/batch', {
+   method: 'POST',
+   headers: {
+     'Authorization': `Bearer ${process.env.FLIXU_API_KEY}`,
+     'Content-Type': 'application/json',
+   },
+   body: JSON.stringify({
+     strings: yourKeyValueObject,
+     source_lang: 'en',
+     target_langs: ['de'],
+   }),
+ });
```

## Environment variable mapping

```diff
- LOKALISE_API_TOKEN=abc123
- LOKALISE_PROJECT_ID=12345.67890
+ FLIXU_API_KEY=flx_your_api_key
```

## Key architectural difference

Lokalise is a key-management platform — you push/pull keys and translations are stored on their servers. Flixu is a translation API — you send text, it returns translations. Your locale files stay in your repo.

This means:
- No more push/pull sync workflows
- Your locale JSON/YAML files are the source of truth
- CI/CD pipelines call Flixu API directly (see `flixu-ci` skill)
