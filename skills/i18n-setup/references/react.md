# React (Vite/CRA) with react-i18next

Complete setup for React apps using Vite or Create React App.

## 1. Install dependencies

```bash
npm install react-i18next i18next i18next-http-backend i18next-browser-languagedetector
```

- `i18next` — core i18n engine
- `react-i18next` — React bindings (hooks, components)
- `i18next-http-backend` — lazy-loads locale files via HTTP (so you don't bundle all languages)
- `i18next-browser-languagedetector` — auto-detects user's preferred language

## 2. Create locale files in `public/locales/`

```
public/locales/
├── en/
│   └── translation.json
├── de/
│   └── translation.json
└── es/
    └── translation.json
```

They live in `public/` so the HTTP backend can load them at runtime without bundling:

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

## 3. Create `src/i18n.ts`

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
    interpolation: {
      escapeValue: false, // React already handles XSS
    },
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
  });

export default i18n;
```

## 4. Import in entry point (`src/main.tsx`)

```typescript
import './i18n'; // Must be imported before App
import App from './App';
```

## 5. Usage in components

```tsx
import { useTranslation } from 'react-i18next';

export function HomePage() {
  const { t, i18n } = useTranslation();

  return (
    <div>
      <h1>{t('common.appName')}</h1>

      {/* Language switcher */}
      <select
        value={i18n.language}
        onChange={(e) => i18n.changeLanguage(e.target.value)}
      >
        <option value="en">English</option>
        <option value="de">Deutsch</option>
        <option value="es">Español</option>
      </select>
    </div>
  );
}
```

## 6. Suspense for loading states

Wrap your app with `Suspense` since translations load asynchronously:

```tsx
import { Suspense } from 'react';

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <MainContent />
    </Suspense>
  );
}
```
