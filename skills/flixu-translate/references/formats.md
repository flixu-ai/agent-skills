# Flixu Translate — Format Reference

## JSON (i18n key-value files)

Use `POST /v1/translate/batch` for JSON locale files.

### Flat JSON
```json
{"greeting": "Hello", "farewell": "Goodbye"}
```

### Nested JSON
```json
{"common": {"greeting": "Hello", "farewell": "Goodbye"}}
```

For nested JSON, flatten to dot-notation before sending, then unflatten the response:
- `common.greeting` → `Hello`

The `scripts/translate.py` script handles this automatically.

## XLIFF (.xliff, .xlf)

Use `POST /v1/translate/document`.

XLIFF is the industry standard for exchanging translations between tools. Flixu preserves:
- Translation unit IDs
- Source and target elements
- Notes and context metadata
- Inline elements (`<ph>`, `<x>`, `<g>`)

## PO/POT (.po, .pot)

Use `POST /v1/translate/document`.

GNU Gettext format used by WordPress, Django, and PHP apps. Flixu handles:
- `msgid` / `msgstr` pairs
- Plural forms (`msgid_plural`, `msgstr[0]`, `msgstr[1]`)
- Context (`msgctxt`)
- Translator comments

## iOS .strings

Use `POST /v1/translate/document`.

```
"key" = "value";
```

Flixu preserves the key-value pair format and handles escape sequences.

## DOCX (.docx)

Use `POST /v1/translate/document`.

Word documents are parsed paragraph-by-paragraph. Flixu preserves:
- Text formatting (bold, italic, underline)
- Headers and footers
- Tables
- Lists

## Subtitles (.srt, .vtt)

Use `POST /v1/translate/document`.

Subtitle files are translated while preserving timing information:
- SRT: sequence numbers + timestamps
- WebVTT: cues + timestamps + positioning
