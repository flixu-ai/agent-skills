# Flixu Assets — Brand Voice Profiles

## What is a Brand Voice profile?

A Brand Voice profile defines how your brand communicates in every language. Without one, translations are technically correct but may not sound like your brand — a casual startup and a formal bank both say "Submit", but the German translation differs ("Absenden" vs. "Einreichen").

## Creating a profile

Navigate to **Assets → Brand Voices → Create** at [app.flixu.ai](https://app.flixu.ai).

### Option 1: Natural language description

Describe your brand in plain text. Flixu generates structured rules from this:

```
We're a developer tools company building for indie hackers.
Tone: friendly, technical, slightly irreverent.
Never use corporate jargon ("leverage", "synergy", "optimize").
For German: use informal "du" form.
For French: use informal "tu" form.
For Japanese: use polite but not overly formal keigo.
Keep UI labels under 30 characters when possible.
```

### Option 2: Structured attributes

| Attribute | Options | Description |
|-----------|---------|-------------|
| **Formality** | formal / informal / neutral | Affects pronoun choice (Sie/du, vous/tu) |
| **Tone** | professional, friendly, playful, serious, technical | Overall communication style |
| **Style** | concise, descriptive, conversational | Sentence structure and length |
| **Anti-patterns** | Specific phrases/patterns to avoid | "Never say 'click here'" |
| **Terminology rules** | Specific word choices | "Always 'workspace', never 'project'" |

## Per-market voice profiles

Different markets often need different voices:

| Market | Typical formality | Notes |
|--------|------------------|-------|
| 🇩🇪 Germany | Formal ("Sie") for B2B, informal ("du") for B2C | B2B software often uses "Sie" |
| 🇫🇷 France | Formal ("vous") default | "Tu" only for very casual brands |
| 🇯🇵 Japan | Polite (です/ます) | Keigo levels vary by industry |
| 🇺🇸 USA | Informal | "You" covers both formal/informal |
| 🇪🇸 Spain | Informal ("tú") | "Usted" feels overly formal for most software |

Create separate Brand Voice profiles per market if your tone varies significantly.

## Best practices

- **Test first**: Translate 10 representative strings and review before applying globally
- **Include anti-patterns**: "Never say X" is as useful as "Say Y"
- **Keep it concise**: 3–5 rules are more effective than 20 — the AI prioritizes the first rules
- **Update after rebrand**: Brand voice changes should immediately update the profile
