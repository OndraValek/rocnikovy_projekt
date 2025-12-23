# Oprava OAuth2 - Redirect URI problém

## Problém
V GitHub OAuth aplikaci máte nastavený callback URL s **dvojitým lomítkem**:
```
http://127.0.0.1:8000//accounts/github/login/callback/
```

To způsobuje chybu "redirect_uri is not associated with this application".

## Řešení

### 1. GitHub OAuth App
1. Jděte na: https://github.com/settings/developers
2. Klikněte na vaši OAuth aplikaci "maturitniProjekt"
3. V poli **"Authorization callback URL"** změňte:
   - ❌ ŠPATNĚ: `http://127.0.0.1:8000//accounts/github/login/callback/`
   - ✅ SPRÁVNĚ: `http://localhost:8000/accounts/github/login/callback/`

4. Klikněte na "Update application"

### 2. Google OAuth App
1. Jděte na: https://console.cloud.google.com/apis/credentials
2. Klikněte na vaši OAuth 2.0 Client ID
3. V sekci **"Authorized redirect URIs"** zkontrolujte:
   - ✅ Mělo by být: `http://localhost:8000/accounts/google/login/callback/`
   - ❌ NESMÍ být: `http://127.0.0.1:8000//accounts/google/login/callback/`

4. Pokud je potřeba, upravte a uložte

### 3. Microsoft OAuth App (Azure AD)
1. Jděte na: https://portal.azure.com/
2. Najděte vaši App Registration
3. V sekci **"Redirect URIs"** zkontrolujte:
   - ✅ Mělo by být: `http://localhost:8000/accounts/microsoft/login/callback/`
   - ❌ NESMÍ být: `http://127.0.0.1:8000//accounts/microsoft/login/callback/`

4. Pokud je potřeba, upravte a uložte

## Důležité poznámky

1. **Používejte `localhost` místo `127.0.0.1`** - Django je nastavený na `localhost:8000`
2. **Žádné dvojité lomítko** - URL musí být: `/accounts/...` ne `//accounts/...`
3. **Ukončovací lomítko** - callback URL by měla končit lomítkem: `/callback/`

## Testování

Po opravě:
1. Restartujte Django server (pokud běží)
2. Zkuste se přihlásit přes OAuth2
3. Mělo by to fungovat bez chyby "redirect_uri mismatch"

## Pokud stále nefunguje

1. Zkontrolujte `.env` soubor - měl by obsahovat správné Client ID a Secret
2. Zkontrolujte Django admin → Social Applications - měly by být správně nastavené
3. Zkontrolujte Django logy pro více informací o chybě


