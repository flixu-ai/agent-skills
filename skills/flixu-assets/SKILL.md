---
name: flixu-assets
description: Manage translation assets — glossaries, translation memories, and brand voices — using the Flixu platform. Use this skill when a developer asks to "create a glossary", "import translation memory", "set up TM", "import TMX", "configure brand voice", "manage translation assets", "add terminology", "create term base", or needs guidance on translation asset strategy (when to use TMs vs glossaries, how many to create, etc.). Also triggers on mentions of "glossary terms", "brand tone", "terminology management", "translation reuse", or even "my translations are inconsistent" — because inconsistent translations are usually a sign that glossaries or brand voice profiles are needed.
---

# Flixu Assets

Manage translation assets — Glossaries, Translation Memories, and Brand Voices — via the Flixu platform. These assets are what transform generic AI translations into brand-consistent, terminology-accurate output. Without them, every translation is independent; with them, the system learns and improves over time.

## When to use which asset

| Asset | Purpose | When to create | Impact |
|-------|---------|----------------|--------|
| **Glossary** | Enforce exact terminology | When you have terms that must be translated a specific way (brand names, product features, legal terms) | Terminology consistency |
| **Translation Memory (TM)** | Reuse previous translations | Builds automatically from approved translations — no action needed to start | Cost savings + consistency |
| **Brand Voice** | Enforce tone and style | When translations should sound a specific way (formal/informal, playful/serious) | Brand consistency |

## Asset strategy recommendations

Different project stages need different asset strategies — starting with too much overhead slows you down, but too little leads to inconsistency at scale:

| Stage | Recommended assets |
|-------|-------------------|
| **Getting started** (< 1K strings) | 1 glossary with core terms (brand name, product features, key UI labels) |
| **Growing** (1K–10K strings) | 1 glossary + TM (auto-builds from translations) |
| **Established** (10K+ strings) | Multiple glossaries per domain + TM + brand voice |
| **Enterprise** (multi-product) | Glossary per product + shared TM + brand voice per market |

## Managing glossaries

### Creating a glossary

Navigate to **Assets → Glossaries → Create Glossary** at [app.flixu.ai](https://app.flixu.ai).

Name it by domain (e.g., "Medical Terms", "E-commerce UI", "Legal") — not by language pair, because one glossary can serve multiple target languages.

### Importing from CSV

**Example:**
Input: "Create a glossary for my e-commerce app with German translations"
Output: Prepare this CSV format:

```csv
source_term,target_term,source_lang,target_lang,notes
Submit,Absenden,en,de,Button text - imperative form
Cancel,Abbrechen,en,de,Button text
Dashboard,Dashboard,en,de,Keep English - brand term
Invoice,Rechnung,en,de,Financial context
Add to cart,In den Warenkorb,en,de,E-commerce action
```

Import at: **Assets → Glossary → Import CSV**

### Glossary best practices

- **Be specific**: "Submit" → "Absenden" (imperative) is better than "Submit" → "Einreichen" (ambiguous)
- **Include context in notes**: "Bank" could mean financial institution or river bank — the note disambiguates
- **Don't over-glossarize**: Only terms that genuinely need enforcement. Over-constraining the AI reduces natural fluency
- **Separate by domain**: Legal terms in one glossary, UI terms in another — you may want different glossaries for different projects
- **Review regularly**: Remove outdated terms, add new product features

## Managing Translation Memory

### How TM works

TM builds automatically from your translations — no manual setup needed:

1. Every approved translation is stored as a TM entry with its source text
2. New translations are compared against TM via semantic vector search
3. Close matches (≥85% similarity) are provided to the AI as context — improving consistency
4. Exact matches (100%) skip the AI pipeline entirely — zero cost, instant response

### Importing from TMX

If migrating from another provider (use the `i18n-migration` skill for the full workflow):

1. Export from your previous tool as TMX format
2. Navigate to **Assets → Translation Memory → Import TMX**
3. Select the TMX file and confirm language pairs

### TM best practices

- **Let it grow naturally**: TM builds from your translations — no need to pre-populate unless migrating
- **Approve quality translations**: Only approved translations enter the TM, so the quality threshold stays high
- **Clean periodically**: Remove entries when terminology changes (e.g., product rebranding)
- **Don't mix unrelated domains**: A medical TM shouldn't influence e-commerce translations

## Managing Brand Voice

### Creating a profile

Navigate to **Assets → Brand Voices → Create** at [app.flixu.ai](https://app.flixu.ai).

| Attribute | Options | Example |
|-----------|---------|---------|
| **Formality** | Formal / Informal / Neutral | "Use 'Sie' in German, 'vous' in French" |
| **Tone** | Professional / Friendly / Playful / Serious | "Warm and approachable, never corporate jargon" |
| **Style** | Concise / Descriptive / Technical / Conversational | "Short, action-oriented sentences for UI" |
| **Anti-patterns** | What to avoid | "Never say 'click here'" |

### Auto-generated profiles

**Example:**
Input: "Set up a brand voice — we're a developer tools company, casual tone, use 'du' in German"
Output: Describe your brand in natural language at the Create Brand Voice screen:

```
We're a developer tools company. Our tone is friendly but technical.
We use 'you' and avoid corporate speak. For German, use informal 'du'
form. Keep UI strings under 40 characters where possible.
```

Flixu generates a structured voice profile from this description.

### Brand voice best practices

- **One voice per market**: German customers might expect formal tone, while US customers prefer casual — create separate profiles
- **Include anti-patterns**: "Never say 'click here'" is as useful as "Say 'select'" — the AI needs to know what to avoid
- **Test with samples**: Translate 10 representative strings and review before applying globally
