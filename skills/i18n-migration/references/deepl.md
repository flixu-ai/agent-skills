# DeepL → Flixu Migration

## Package replacement

```diff
- npm install deepl-node
+ # No Flixu SDK needed — uses standard fetch
```

```diff
- import { Translator } from 'deepl-node';
```

## API call rewrite

### Text translation

```diff
- const translator = new Translator(process.env.DEEPL_AUTH_KEY);
- const result = await translator.translateText(text, null, 'de');
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

### Document translation

```diff
- const result = await translator.translateDocument(
-   'input.docx',
-   'output.docx',
-   null,
-   'de'
- );
+ const formData = new FormData();
+ formData.append('file', fs.createReadStream('input.docx'));
+ formData.append('source_lang', 'en');
+ formData.append('target_lang', 'de');
+ const response = await fetch('https://api.flixu.ai/v1/translate/document', {
+   method: 'POST',
+   headers: { 'Authorization': `Bearer ${process.env.FLIXU_API_KEY}` },
+   body: formData,
+ });
```

### Glossary migration

DeepL glossaries are downloadable as TSV. Convert to CSV for Flixu:
```bash
# Convert DeepL TSV to Flixu CSV
echo "source_term,target_term,source_lang,target_lang,notes" > glossary.csv
cat deepl_glossary.tsv | awk -F'\t' '{print $1","$2",en,de,"}' >> glossary.csv
```

## Environment variable mapping

```diff
- DEEPL_AUTH_KEY=abc123
+ FLIXU_API_KEY=flx_your_api_key
```

## Language code mapping

| Language | DeepL | Flixu |
|----------|-------|-------|
| English (US) | `EN-US` | `en` |
| English (GB) | `EN-GB` | `en` |
| Portuguese (BR) | `PT-BR` | `pt` |
| Portuguese (PT) | `PT-PT` | `pt` |
| Chinese | `ZH` | `zh` |
| Norwegian | `NB` | `nb` |

DeepL uses uppercase codes with region variants. Flixu uses lowercase ISO 639-1.
