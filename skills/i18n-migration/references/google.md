# Google Cloud Translation → Flixu Migration

## Package replacement

```diff
- npm install @google-cloud/translate
+ # No Flixu SDK needed — uses standard fetch
```

## API call rewrite

### Text translation (v3)

```diff
- import { TranslationServiceClient } from '@google-cloud/translate';
- const client = new TranslationServiceClient();
- const [response] = await client.translateText({
-   parent: `projects/${projectId}/locations/global`,
-   contents: [text],
-   targetLanguageCode: 'de',
-   sourceLanguageCode: 'en',
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

### Text translation (v2 / simple)

```diff
- const { Translate } = require('@google-cloud/translate').v2;
- const translate = new Translate({ projectId });
- const [translation] = await translate.translate(text, 'de');
+ const response = await fetch('https://api.flixu.ai/v1/translate', {
+   method: 'POST',
+   headers: {
+     'Authorization': `Bearer ${process.env.FLIXU_API_KEY}`,
+     'Content-Type': 'application/json',
+   },
+   body: JSON.stringify({ text, source_lang: 'en', target_lang: 'de' }),
+ });
+ const { data } = await response.json();
+ const translation = data.translation;
```

### Batch translation

```diff
- const [responses] = await client.batchTranslateText({
-   parent: `projects/${projectId}/locations/global`,
-   sourceLanguageCode: 'en',
-   targetLanguageCodes: ['de', 'fr'],
-   inputConfigs: [{ gcsSource: { inputUri: 'gs://...' } }],
-   outputConfig: { gcsDestination: { outputUriPrefix: 'gs://...' } },
- });
+ const response = await fetch('https://api.flixu.ai/v1/translate/batch', {
+   method: 'POST',
+   headers: {
+     'Authorization': `Bearer ${process.env.FLIXU_API_KEY}`,
+     'Content-Type': 'application/json',
+   },
+   body: JSON.stringify({
+     strings: { key1: 'Hello', key2: 'Goodbye' },
+     source_lang: 'en',
+     target_langs: ['de', 'fr'],
+   }),
+ });
```

## Environment variable mapping

```diff
- GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
- GOOGLE_CLOUD_PROJECT=my-project-id
+ FLIXU_API_KEY=flx_your_api_key
```

## Language code mapping

| Language | Google | Flixu |
|----------|--------|-------|
| Chinese (Simplified) | `zh-CN` | `zh` |
| Chinese (Traditional) | `zh-TW` | `zh-TW` |
| Norwegian | `no` | `nb` |
| Portuguese | `pt` | `pt` |

Google uses BCP-47 codes. Flixu uses ISO 639-1 (lowercase, no region for most).
