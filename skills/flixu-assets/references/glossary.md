# Flixu Assets — Glossary Management

## Creating a glossary

Navigate to **Assets → Glossaries → Create Glossary** at [app.flixu.ai](https://app.flixu.ai).

### Naming convention

Name glossaries by domain, not by language pair:
- ✅ "Medical Terms", "E-commerce UI", "Legal"
- ❌ "English-German", "EN-DE translations"

One glossary serves all target languages — the system matches source terms regardless of target.

## CSV import format

```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text - imperative form
Cancel,Abbrechen,en,de,Button text
Dashboard,Dashboard,en,de,Keep English - brand term
Invoice,Rechnung,en,de,Financial context
Add to cart,In den Warenkorb,en,de,E-commerce action
```

### Required columns
- `source_term` — The original term
- `target_term` — The required translation
- `source_lang` — ISO 639-1 code
- `target_lang` — ISO 639-1 code

### Optional columns
- `notes` — Context for disambiguation (strongly recommended for ambiguous terms)

## Best practices

### What to glossarize
- **Brand names** that should never be translated (or always translated a specific way)
- **Product feature names** — ensure "Workspace" is always "Arbeitsbereich" in German
- **UI action verbs** — "Submit" → "Absenden" (imperative), not "Einreichen"
- **Legal/regulatory terms** — exact translation required by compliance
- **Technical terms** — maintain consistency across documentation

### What NOT to glossarize
- Common words with obvious translations ("Hello", "Settings")
- Terms where context determines the best translation
- Entire phrases or sentences — glossaries are for terms, not content

### Review cycle
1. **Monthly**: Add new product features and terms
2. **Quarterly**: Remove deprecated terms, update changed terminology
3. **After rebranding**: Update all brand-related terms
