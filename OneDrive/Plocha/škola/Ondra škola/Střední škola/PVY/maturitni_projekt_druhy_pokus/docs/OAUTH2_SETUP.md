# Nastavení OAuth2 autentizace

Tento projekt podporuje OAuth2 autentizaci přes Google, GitHub a Microsoft pomocí django-allauth.

## Požadavky

- django-allauth je již nainstalován v `requirements.txt`
- Všechny potřebné aplikace jsou přidány do `INSTALLED_APPS`
- Šablony pro přihlášení a registraci jsou vytvořeny s OAuth2 tlačítky

## Nastavení OAuth2 poskytovatelů

### 1. Google OAuth2

1. Jděte na [Google Cloud Console](https://console.cloud.google.com/)
2. Vytvořte nový projekt nebo vyberte existující
3. Povolte Google+ API
4. Vytvořte OAuth 2.0 Client ID:
   - Jděte na "Credentials" → "Create Credentials" → "OAuth client ID"
   - Vyberte "Web application"
   - Přidejte Authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/` (pro vývoj)
     - `https://yourdomain.com/accounts/google/login/callback/` (pro produkci)
5. Zkopírujte Client ID a Client Secret

### 2. GitHub OAuth2

1. Jděte na [GitHub Developer Settings](https://github.com/settings/developers)
2. Klikněte na "New OAuth App"
3. Vyplňte:
   - **Application name**: Název vaší aplikace
   - **Homepage URL**: `http://localhost:8000` (pro vývoj)
   - **Authorization callback URL**: `http://localhost:8000/accounts/github/login/callback/`
4. Zkopírujte Client ID a Client Secret

### 3. Microsoft OAuth2 (Azure AD)

1. Jděte na [Azure Portal](https://portal.azure.com/)
2. Vytvořte novou aplikaci v Azure Active Directory:
   - Jděte na "App registrations" → "New registration"
   - Vyplňte název aplikace
   - Vyberte "Accounts in any organizational directory and personal Microsoft accounts"
   - Přidejte Redirect URI: `http://localhost:8000/accounts/microsoft/login/callback/`
3. V "Certificates & secrets" vytvořte nový Client Secret
4. Zkopírujte Application (client) ID a Client Secret

## Konfigurace environment variables

Vytvořte soubor `.env` v kořenovém adresáři projektu (nebo použijte existující) a přidejte:

```env
# Google OAuth2
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth2
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Microsoft OAuth2
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
```

**DŮLEŽITÉ:** Nikdy necommitněte `.env` soubor do Gitu! Ujistěte se, že je v `.gitignore`.

## Migrace databáze

Po přidání OAuth2 poskytovatelů je potřeba vytvořit migrace:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Vytvoření Social Applications v Django Admin

1. Spusťte vývojový server: `python manage.py runserver`
2. Jděte na `/django-admin/` a přihlaste se jako superuser
3. V sekci "Social Accounts" → "Social Applications" vytvořte nové aplikace:
   - **Google**: Provider = Google, Client ID a Secret z .env
   - **GitHub**: Provider = GitHub, Client ID a Secret z .env
   - **Microsoft**: Provider = Microsoft, Client ID a Secret z .env
4. Pro každou aplikaci vyberte správný Site (obvykle "example.com")

**Alternativně** můžete vytvořit Social Applications programově pomocí Django shell nebo management commandu.

## Testování

1. Spusťte server: `python manage.py runserver`
2. Jděte na `/accounts/login/`
3. Měli byste vidět tlačítka pro přihlášení přes Google, GitHub a Microsoft
4. Klikněte na jedno z tlačítek a otestujte OAuth2 flow

## Řešení problémů

### Tlačítka se nezobrazují
- Zkontrolujte, že jsou poskytovatelé přidáni do `INSTALLED_APPS`
- Zkontrolujte, že jsou vytvořeny Social Applications v Django Admin
- Zkontrolujte, že jsou správně nastaveny environment variables

### Chyba "Redirect URI mismatch"
- Zkontrolujte, že Redirect URI v OAuth2 aplikaci odpovídá URL v Django
- Pro vývoj: `http://localhost:8000/accounts/{provider}/login/callback/`
- Pro produkci: `https://yourdomain.com/accounts/{provider}/login/callback/`

### Uživatel se nemůže přihlásit
- Zkontrolujte, že email z OAuth2 poskytovatele je dostupný
- Zkontrolujte logy Django pro více informací
- Zkontrolujte, že `SOCIALACCOUNT_AUTO_SIGNUP = True` v settings

## Produkční nasazení

Pro produkci:
1. Změňte `ACCOUNT_EMAIL_VERIFICATION` na `'mandatory'`
2. Nastavte správné Redirect URIs u všech OAuth2 poskytovatelů
3. Použijte HTTPS (OAuth2 vyžaduje HTTPS v produkci)
4. Zkontrolujte, že všechny environment variables jsou nastaveny na produkčním serveru

