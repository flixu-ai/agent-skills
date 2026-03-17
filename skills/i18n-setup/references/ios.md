# iOS / macOS with .strings

Complete setup for Swift apps using Apple's built-in localization.

## 1. Create `.lproj/` directories

```
YourApp/
├── Base.lproj/
│   └── Localizable.strings
├── en.lproj/
│   └── Localizable.strings
├── de.lproj/
│   └── Localizable.strings
└── es.lproj/
    └── Localizable.strings
```

## 2. Format for Localizable.strings

```
/* Common section - used across the app */
"common.appName" = "My App";
"common.loading" = "Loading...";
"common.error" = "Something went wrong";

/* Navigation */
"navigation.home" = "Home";
"navigation.about" = "About";
"navigation.settings" = "Settings";
```

Use dot-notation for namespacing — keeps keys organized as the app grows.

## 3. Usage in Swift

```swift
// Basic usage
Text(NSLocalizedString("common.appName", comment: "App name"))

// SwiftUI shorthand (iOS 16+)
Text("common.appName")

// With String Catalogs (Xcode 15+, recommended)
// Just use String("key") and Xcode auto-generates the catalog
```

## 4. Plurals with .stringsdict

Create `Localizable.stringsdict` for plurals:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>items_count</key>
  <dict>
    <key>NSStringLocalizedFormatKey</key>
    <string>%#@count@</string>
    <key>count</key>
    <dict>
      <key>NSStringFormatSpecTypeKey</key>
      <string>NSStringPluralRuleType</string>
      <key>NSStringFormatValueTypeKey</key>
      <string>d</string>
      <key>zero</key>
      <string>No items</string>
      <key>one</key>
      <string>1 item</string>
      <key>other</key>
      <string>%d items</string>
    </dict>
  </dict>
</dict>
</plist>
```

## 5. Add languages in Xcode

1. Project → Info → Localizations → `+`
2. Select language
3. Xcode auto-generates `.lproj/` directories
