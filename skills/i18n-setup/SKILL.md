---
name: i18n-setup
description: Set up internationalization (i18n) file structure, routing, and configuration for any framework. Use this skill whenever a developer asks to "add i18n", "set up localization", "internationalize my app", "add multi-language support", "configure next-intl", "set up react-i18next", "add translations to my app", or needs help structuring locale files, setting up translation routing, or choosing an i18n library. Also triggers on mentions of "locale", "messages directory", "translation files", or "language switching" in the context of project setup.
---

# i18n Setup

Set up a complete internationalization file structure for any framework. This skill handles library selection, directory structure, routing configuration, and initial locale scaffolding.

## When to use this skill

- Developer wants to add multi-language support to an existing or new application
- Developer needs help choosing between i18n libraries (next-intl vs react-i18next vs i18next, etc.)
- Developer needs locale directory structure and file organization guidance
- Developer is starting a new project and wants i18n built in from day one

## Framework detection

Before starting, detect the framework by checking for:

| Signal | Framework |
|--------|-----------|
| `next.config.*` or `app/` directory | **Next.js** (App Router) |
| `next.config.*` + `pages/` directory | **Next.js** (Pages Router) |
| `vite.config.*` or `package.json` with `react` | **React** (Vite/CRA) |
| `pubspec.yaml` with `flutter` | **Flutter** |
| `Gemfile` with `rails` | **Ruby on Rails** |
| `*.xcodeproj` or `Package.swift` | **iOS/macOS (Swift)** |
| `build.gradle` with `android` | **Android** |

If you can't detect the framework, ask the developer.

## Setup procedures

### Next.js (App Router) with next-intl

This is the recommended setup for Next.js 13+ applications.

1. **Install dependency**:
   ```bash
   npm install next-intl
   ```

2. **Create locale files** in `messages/`:
   ```
   messages/
   ├── en.json    ← source locale
   ├── de.json    ← target locales
   └── es.json
   ```

   Each file starts with a minimal structure:
   ```json
   {
     "common": {
       "appName": "My App",
       "loading": "Loading...",
       "error": "Something went wrong"
     },
     "navigation": {
       "home": "Home",
       "about": "About",
       "settings": "Settings"
     }
   }
   ```

3. **Create `src/i18n/routing.ts`**:
   ```typescript
   import { defineRouting } from 'next-intl/routing';

   export const routing = defineRouting({
     locales: ['en', 'de', 'es'],
     defaultLocale: 'en',
   });
   ```

4. **Create `src/i18n/request.ts`**:
   ```typescript
   import { getRequestConfig } from 'next-intl/server';
   import { routing } from './routing';

   export default getRequestConfig(async ({ requestLocale }) => {
     let locale = await requestLocale;
     if (!locale || !routing.locales.includes(locale as typeof routing.locales[number])) {
       locale = routing.defaultLocale;
     }
     return {
       locale,
       messages: (await import(`../../../messages/${locale}.json`)).default,
     };
   });
   ```

5. **Create `src/middleware.ts`**:
   ```typescript
   import createMiddleware from 'next-intl/middleware';
   import { routing } from './i18n/routing';

   export default createMiddleware(routing);

   export const config = {
     matcher: ['/', '/(de|es|en)/:path*'],
   };
   ```

6. **Update `app/[locale]/layout.tsx`**:
   ```tsx
   import { NextIntlClientProvider } from 'next-intl';
   import { getMessages } from 'next-intl/server';

   export default async function LocaleLayout({
     children,
     params,
   }: {
     children: React.ReactNode;
     params: Promise<{ locale: string }>;
   }) {
     const { locale } = await params;
     const messages = await getMessages();

     return (
       <html lang={locale}>
         <body>
           <NextIntlClientProvider messages={messages}>
             {children}
           </NextIntlClientProvider>
         </body>
       </html>
     );
   }
   ```

7. **Usage in components**:
   ```tsx
   import { useTranslations } from 'next-intl';

   export default function HomePage() {
     const t = useTranslations('common');
     return <h1>{t('appName')}</h1>;
   }
   ```

### React (Vite) with react-i18next

1. **Install dependencies**:
   ```bash
   npm install react-i18next i18next i18next-http-backend i18next-browser-languagedetector
   ```

2. **Create locale files** in `public/locales/`:
   ```
   public/locales/
   ├── en/
   │   └── translation.json
   ├── de/
   │   └── translation.json
   └── es/
       └── translation.json
   ```

3. **Create `src/i18n.ts`**:
   ```typescript
   import i18n from 'i18next';
   import { initReactI18next } from 'react-i18next';
   import HttpBackend from 'i18next-http-backend';
   import LanguageDetector from 'i18next-browser-languagedetector';

   i18n
     .use(HttpBackend)
     .use(LanguageDetector)
     .use(initReactI18next)
     .init({
       fallbackLng: 'en',
       supportedLngs: ['en', 'de', 'es'],
       interpolation: { escapeValue: false },
     });

   export default i18n;
   ```

4. **Import in entry point** (`src/main.tsx`):
   ```typescript
   import './i18n';
   ```

### Flutter with ARB

1. **Add dependencies** to `pubspec.yaml`:
   ```yaml
   dependencies:
     flutter_localizations:
       sdk: flutter
     intl: any

   flutter:
     generate: true
   ```

2. **Create `l10n.yaml`**:
   ```yaml
   arb-dir: lib/l10n
   template-arb-file: app_en.arb
   output-localization-file: app_localizations.dart
   ```

3. **Create ARB files** in `lib/l10n/`:
   ```json
   {
     "@@locale": "en",
     "appTitle": "My App",
     "@appTitle": { "description": "The application title" },
     "hello": "Hello {name}",
     "@hello": { "placeholders": { "name": { "type": "String" } } }
   }
   ```

### iOS / macOS with .strings

1. **Create `.lproj/` directories**:
   ```
   Base.lproj/Localizable.strings
   en.lproj/Localizable.strings
   de.lproj/Localizable.strings
   ```

2. **Format**:
   ```
   "common.appName" = "My App";
   "common.loading" = "Loading...";
   ```

## After setup

Once the i18n structure is in place, suggest the developer:

1. **Translate**: Use the `flixu-translate` skill to translate locale files
2. **Audit**: Use the `translation-qa` skill to find missing keys
3. **Automate**: Use the `flixu-ci` skill to auto-translate on push

## RTL considerations

If any target locale is RTL (Arabic, Hebrew, Persian, Urdu), additionally:
- Set `dir="rtl"` on the `<html>` element based on locale
- Use CSS logical properties (`margin-inline-start` instead of `margin-left`)
- Test layout with RTL content early
