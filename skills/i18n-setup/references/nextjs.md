# Next.js (App Router) with next-intl

Complete setup for Next.js 13+ applications using `next-intl`.

## 1. Install dependency

```bash
npm install next-intl
```

## 2. Create locale files in `messages/`

```
messages/
├── en.json    ← source locale
├── de.json    ← target locales (copy structure, translate values)
└── es.json
```

Each file starts with a minimal structure — namespace by feature:

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

## 3. Create `src/i18n/routing.ts`

Define supported locales in one place — every other file imports from here:

```typescript
import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  locales: ['en', 'de', 'es'],
  defaultLocale: 'en',
});
```

## 4. Create `src/i18n/request.ts`

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

## 5. Create `src/middleware.ts`

```typescript
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  // Match all pathnames except for API routes, _next, and static files
  matcher: ['/', '/(de|es|en)/:path*'],
};
```

## 6. Update `app/[locale]/layout.tsx`

Wrap your app with the provider — this makes `useTranslations` available in all client components:

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

## 7. Usage in components

```tsx
// Server Component (zero bundle impact)
import { useTranslations } from 'next-intl';

export default function HomePage() {
  const t = useTranslations('common');
  return <h1>{t('appName')}</h1>;
}
```

```tsx
// Client Component
'use client';
import { useTranslations } from 'next-intl';

export function SearchBar() {
  const t = useTranslations('search');
  return <input placeholder={t('placeholder')} />;
}
```

## 8. Update `next.config.ts`

```typescript
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin();

const nextConfig = {};

export default withNextIntl(nextConfig);
```
