---
name: flixu-assets
description: Manage translation assets — glossaries, translation memories, and brand voices — on the Flixu platform. Use when a developer asks to "create a glossary", "import TM", "set up translation memory", "configure brand voice", or "add terminology". Also triggers on "inconsistent translations", "glossary terms", or "translation reuse". Do NOT use for translating content (use flixu-translate) or i18n setup (use i18n-setup).
metadata:
  author: Flixu AI
  version: 1.0.0
  category: localization
  tags: [glossary, translation-memory, brand-voice, assets, terminology]
---

# Flixu Assets

Manage translation assets — Glossaries, Translation Memories, and Brand Voices — via the Flixu platform. These assets transform generic AI translations into brand-consistent, terminology-accurate output.

## Detailed references

For deep-dive guidance on specific asset types:
- **`references/glossary.md`** — CSV format spec, naming conventions, what to/not to glossarize, review cycles
- **`references/brand-voice.md`** — Per-market voice profiles, natural language vs structured creation, formality rules by country

## Instructions

### Step 1: Assess the project's asset needs

| Stage | Recommended assets |
|-------|-------------------|
| Getting started (< 1K strings) | 1 glossary with core terms |
| Growing (1K–10K strings) | 1 glossary + TM (auto-builds) |
| Established (10K+ strings) | Multiple glossaries per domain + TM + brand voice |
| Enterprise (multi-product) | Glossary per product + shared TM + brand voice per market |

Expected output: Recommended asset strategy based on project size.

### Step 2: Create glossary (if needed)

Navigate to **Assets → Glossaries → Create Glossary** at app.flixu.ai.

Name by domain ("Medical Terms", "E-commerce UI"), not by language pair.

For bulk import, prepare a CSV:
```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text - imperative form
Dashboard,Dashboard,en,de,Keep English - brand term
```

Import at **Assets → Glossary → Import CSV**.

For detailed guidance, read `references/glossary.md`.

Expected output: Glossary created and populated with core terms.

### Step 3: Set up Translation Memory (if needed)

TM builds automatically — no manual setup required:
1. Every approved translation is stored
2. Future translations are compared via semantic vector search
3. Close matches (≥85%) are suggested as AI context
4. Exact matches (100%) skip the AI pipeline — zero cost

For importing from another provider, export as TMX and import at **Assets → Translation Memory → Import TMX**.

Expected output: TM active and accumulating entries from translations.

### Step 4: Create Brand Voice profile (if needed)

Navigate to **Assets → Brand Voices → Create** at app.flixu.ai.

Describe the brand in natural language:
```
We're a developer tools company. Friendly but technical tone.
Use informal "du" in German, "tu" in French.
Never use corporate jargon like "leverage" or "synergy".
```

Flixu generates structured rules from this description.

For per-market profiles and detailed options, read `references/brand-voice.md`.

Expected output: Brand voice profile created and applied to all future translations.

## Examples

### Example 1: Set up glossary for an e-commerce app

User says: "Create a glossary for my e-commerce app with German translations"

Actions:
1. Assess: growing app (< 10K strings) → recommend 1 glossary + TM
2. Create CSV with core terms: Submit → Absenden, Add to cart → In den Warenkorb
3. Guide import at Assets → Glossary → Import CSV

Result: Glossary "E-commerce UI" created with 15 core terms. Future translations use these terms.

### Example 2: Fix inconsistent translations

User says: "My translations are inconsistent — 'workspace' gets translated differently each time"

Actions:
1. Identify this as a glossary problem
2. Create glossary entry: "workspace" → "Arbeitsbereich" (de), with note "Always use this term"
3. Explain how the glossary enforces consistency in future translations

Result: Glossary entry created. All future translations of "workspace" consistently use "Arbeitsbereich".

### Example 3: Set up formal German brand voice

User says: "Our German translations should use the formal 'Sie' form"

Actions:
1. Create a Brand Voice profile for the German market
2. Set formality to "formal", include rule: "Always use 'Sie' form"
3. Recommend testing with 10 sample translations

Result: Brand voice profile active. All German translations use formal "Sie" form.

## Troubleshooting

### Error: Glossary terms not appearing in translation output

Cause: Glossary not attached to the translation request.
Solution: Include `glossary_ids` parameter in the translation API call. Use the `flixu-translate` skill which handles this automatically.

### Error: Brand voice produces unexpected tone

Cause: Conflicting rules in the profile description.
Solution: Keep rules to 3-5 clear statements. Contradictory rules (e.g., "be casual" + "use formal pronouns") confuse the AI.

### Error: TM not matching similar strings

Cause: TM is still building — needs more approved translations.
Solution: TM improves with volume. After 100+ translations, match rates increase significantly.
