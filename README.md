# Flixu Agent Skills

> AI coding agent skills for localization and internationalization.

Install these skills into your AI coding agent (Claude Code, Cursor, GitHub Copilot, Cline, and 15+ more) to get localization superpowers — from setting up i18n architecture to automating translation workflows.

## Quick Start

```bash
# Install all skills
npx skills add flixu-ai/agent-skills

# Install a specific skill
npx skills add flixu-ai/agent-skills --skill flixu-translate
```

## Prerequisites

1. **Flixu account** — [Sign up at flixu.ai](https://flixu.ai)
2. **API key** — Create at [app.flixu.ai/settings/api-keys](https://app.flixu.ai/settings/api-keys)
3. Set your API key:
   ```bash
   export FLIXU_API_KEY=flx_your_api_key
   ```

## Available Skills

### 🏗️ Localization Architecture

| Skill | Description |
|-------|-------------|
| [**i18n-setup**](skills/i18n-setup) | Set up i18n file structure, routing, and configuration for Next.js, React, Flutter, Rails, iOS, and more |
| [**i18n-migration**](skills/i18n-migration) | Migrate from DeepL, Google Translate, Lokalise, or Phrase to Flixu |

### 🌐 Translation & Quality

| Skill | Description |
|-------|-------------|
| [**flixu-translate**](skills/flixu-translate) | Full translation workflow: format detection, endpoint selection, output file writing to locale directories |
| [**translation-qa**](skills/translation-qa) | Audit your codebase for missing translations, duplicate keys, inconsistent interpolations, and hardcoded strings |

### 🚀 Automation & CI/CD

| Skill | Description |
|-------|-------------|
| [**flixu-ci**](skills/flixu-ci) | Generate GitHub Actions / GitLab CI configs for auto-translation on push with quality gates |
| [**flixu-assets**](skills/flixu-assets) | Manage translation assets — glossaries, translation memories, and brand voices |

## Usage Examples

Once installed, just ask your AI agent naturally:

```
"Set up i18n for my Next.js app with English, German, and Spanish"
```

```
"Translate my en.json to German and French"
```

```
"Find all untranslated strings in my app"
```

```
"Create a GitHub Action that auto-translates on push"
```

```
"Create a glossary for my medical app"
```

```
"Migrate from DeepL to Flixu"
```

## Documentation

Full documentation at [docs.flixu.ai](https://docs.flixu.ai):

- [Agent Skills Overview](https://docs.flixu.ai/developer-guide/agent-skills/overview)
- [Getting Started](https://docs.flixu.ai/developer-guide/agent-skills/getting-started)
- [API Reference](https://docs.flixu.ai/api-reference/overview)

## Compatibility

These skills work with any AI coding agent that supports the [skills standard](https://skills.sh):

- Claude Code
- Cursor
- GitHub Copilot
- Cline
- Windsurf
- Amp
- Codex
- Warp
- Gemini CLI
- OpenCode
- Kimi Code CLI
- And more...

## License

MIT — see [LICENSE](LICENSE).

## Links

- **Website**: [flixu.ai](https://flixu.ai)
- **App**: [app.flixu.ai](https://app.flixu.ai)
- **API Docs**: [docs.flixu.ai](https://docs.flixu.ai)
- **LinkedIn**: [Flixu AI](https://www.linkedin.com/company/flixu-ai)
