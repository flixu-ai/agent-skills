---
name: flixu-assets
description: Manage translation assets — glossaries, translation memories, and brand voices — using the Flixu API. Use this skill when a developer asks to "create a glossary", "import translation memory", "set up TM", "import TMX", "configure brand voice", "manage translation assets", "add terminology", "create term base", or needs guidance on translation asset strategy (when to use TMs vs glossaries, how many to create, etc.). Also triggers on mentions of "glossary terms", "brand tone", "terminology management", or "translation reuse".
---

# Flixu Assets

Manage translation assets — Glossaries, Translation Memories, and Brand Voices — via the Flixu platform. These assets improve translation quality, consistency, and cost efficiency.

## When to use which asset

| Asset | Purpose | When to create | Impact |
|-------|---------|----------------|--------|
| **Glossary** | Enforce exact terminology | When you have terms that MUST be translated a specific way (brand names, features, legal terms) | Consistency |
| **Translation Memory (TM)** | Reuse previous translations | When you've been translating content and want to reuse approved translations | Cost savings + consistency |
| **Brand Voice** | Enforce tone and style | When translations should sound a specific way (formal/informal, playful/serious) | Brand consistency |

## Asset strategy recommendations

Based on project size:

| Stage | Recommended assets |
|-------|--------------------|
| **Getting started** (< 1K strings) | 1 glossary with core terms |
| **Growing** (1K–10K strings) | 1 glossary + TM (auto-builds from translations) |
| **Established** (10K+ strings) | Multiple glossaries per domain + TM + brand voice |
| **Enterprise** (multi-product) | Glossary per product + shared TM + brand voice per market |

## Managing glossaries

### Creating a glossary

Glossaries are created and managed via the Flixu web app at [app.flixu.ai/assets/glossary](https://app.flixu.ai/assets/glossary).

**Steps:**
1. Navigate to **Assets → Glossaries → Create Glossary**
2. Name it descriptively (e.g., "Medical Terms", "E-commerce", "Legal")
3. Add terms manually or import from CSV

### Importing glossary from CSV

Prepare a CSV file:

```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text - imperative form
Cancel,Abbrechen,en,de,Button text
Dashboard,Dashboard,en,de,Keep English - brand term
Invoice,Rechnung,en,de,Financial context
```

Import via the web app: **Assets → Glossary → Import CSV**

### Glossary best practices

- **Be specific**: "Submit" → "Absenden" is better than "Submit" → "Einreichen" (which could mean either)
- **Include context**: Add notes for ambiguous terms
- **Don't over-glossarize**: Only terms that MUST be translated a specific way. Let the AI handle the rest.
- **Separate by domain**: Legal terms in one glossary, UI terms in another
- **Review regularly**: Remove outdated terms, add new product features

## Managing Translation Memory

### How TM works in Flixu

Translation Memory builds automatically:
1. Every approved translation is stored as a TM entry
2. Future translations are compared against TM via semantic search
3. Close matches (≥85% similarity) are suggested to the AI as context
4. Exact matches (100%) skip the AI pipeline entirely — zero cost

### Importing TM from TMX

If you have translations from a previous provider:

1. Export from your previous tool as TMX format
2. Navigate to **Assets → Translation Memory → Import TMX**
3. Select the TMX file and confirm language pairs

### TM best practices

- **Let it grow naturally**: TM builds from your translations — no need to pre-populate
- **Approve quality translations**: Only approved translations enter the TM
- **Clean periodically**: Remove outdated entries when terminology changes
- **Don't mix domains**: Keep separate TMs if you have very different content types

## Managing Brand Voice

### Creating a brand voice profile

Brand Voice profiles are created at [app.flixu.ai/assets/brand-voices](https://app.flixu.ai/assets/brand-voices).

**Define these attributes:**

| Attribute | Options | Example |
|-----------|---------|---------|
| **Formality** | Formal / Informal / Neutral | "Use 'Sie' form in German, 'vous' in French" |
| **Tone** | Professional / Friendly / Playful / Serious | "Warm and approachable, never corporate jargon" |
| **Style** | Concise / Descriptive / Technical / Conversational | "Short, action-oriented sentences for UI" |
| **Terminology** | Specific rules | "Always 'workspace' never 'project'" |

### Auto-generated brand profiles

Describe your brand in natural language, and Flixu generates a structured voice profile:

```
"We're a developer tools company. Our tone is friendly but technical. 
We use 'you' and avoid corporate speak. For German, use informal 'du' 
form. Keep UI strings under 40 characters where possible."
```

This generates rules that are applied to every translation.

### Brand voice best practices

- **One voice per market**: German customers might expect formal tone, while US customers prefer casual
- **Include anti-patterns**: "Never say 'click here'" is as useful as "Say 'select'"
- **Test with samples**: Translate 10 representative strings and review before applying globally
