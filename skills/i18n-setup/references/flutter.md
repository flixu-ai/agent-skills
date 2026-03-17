# Flutter with ARB

Complete setup for Flutter apps using the built-in l10n system.

## 1. Add dependencies to `pubspec.yaml`

```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: any

flutter:
  generate: true
```

`flutter_localizations` provides material/cupertino translations.
`intl` provides date/number formatting. `generate: true` enables code generation.

## 2. Create `l10n.yaml` in project root

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

## 3. Create ARB files in `lib/l10n/`

Template file (`app_en.arb`):
```json
{
  "@@locale": "en",
  "appTitle": "My App",
  "@appTitle": {
    "description": "The application title"
  },
  "hello": "Hello {name}",
  "@hello": {
    "description": "Greeting with name",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "Alice"
      }
    }
  },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Number of items",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  }
}
```

Target files (`app_de.arb`):
```json
{
  "@@locale": "de",
  "appTitle": "Meine App",
  "hello": "Hallo {name}",
  "itemCount": "{count, plural, =0{Keine Elemente} =1{1 Element} other{{count} Elemente}}"
}
```

## 4. Update `MaterialApp`

```dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

MaterialApp(
  localizationsDelegates: AppLocalizations.localizationsDelegates,
  supportedLocales: AppLocalizations.supportedLocales,
  home: const MyHomePage(),
);
```

## 5. Usage

```dart
// Access translations
final l10n = AppLocalizations.of(context)!;
Text(l10n.appTitle);
Text(l10n.hello('Alice'));
Text(l10n.itemCount(5));
```

## 6. Run code generation

```bash
flutter gen-l10n
```

This generates Dart classes from your ARB files. Run after adding/modifying locale files.
