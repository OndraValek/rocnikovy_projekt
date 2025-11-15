# Podrobný návod - Nastavení OAuth2 krok za krokem

Tento návod vás provede celým procesem nastavení OAuth2 autentizace pro Google, GitHub a Microsoft.

---

## KROK 1: Vytvoření OAuth2 aplikací u poskytovatelů

### 1.1 Google OAuth2

1. **Jděte na Google Cloud Console:**
   - Otevřete: https://console.cloud.google.com/
   - Přihlaste se svým Google účtem

2. **Vytvořte nebo vyberte projekt:**
   - V horní liště klikněte na dropdown s názvem projektu
   - Klikněte na "NEW PROJECT"
   - Zadejte název (např. "Maturitní projekt")
   - Klikněte na "CREATE"

3. **Povolte Google+ API:**
   - V levém menu: "APIs & Services" → "Library"
   - Vyhledejte "Google+ API" nebo "Google Identity"
   - Klikněte na "ENABLE"

4. **Vytvořte OAuth 2.0 Client ID:**
   - V levém menu: "APIs & Services" → "Credentials"
   - Klikněte na "CREATE CREDENTIALS" → "OAuth client ID"
   - Pokud se zobrazí "Configure consent screen", klikněte na "CONFIGURE CONSENT SCREEN"
     - Vyberte "External" (pro testování)
     - Vyplňte App name: "Maturitní projekt"
     - Vyplňte User support email: váš email
     - Klikněte "SAVE AND CONTINUE" (3x)
   - Vraťte se na "Credentials"
   - Klikněte "CREATE CREDENTIALS" → "OAuth client ID"
   - Vyberte "Web application"
   - Zadejte název: "Maturitní projekt - Web"
   - **DŮLEŽITÉ:** Přidejte "Authorized redirect URIs":
     ```
     http://localhost:8000/accounts/google/login/callback/
     ```
   - Klikněte "CREATE"
   - **Zkopírujte si Client ID a Client Secret** (budete je potřebovat později)

### 1.2 GitHub OAuth2

1. **Jděte na GitHub Developer Settings:**
   - Otevřete: https://github.com/settings/developers
   - Přihlaste se svým GitHub účtem

2. **Vytvořte novou OAuth App:**
   - Klikněte na "OAuth Apps" v levém menu
   - Klikněte na "New OAuth App"

3. **Vyplňte formulář:**
   - **Application name:** Maturitní projekt (nebo jakýkoliv název)
   - **Homepage URL:** `http://localhost:8000`
   - **Authorization callback URL:** `http://localhost:8000/accounts/github/login/callback/`
   - Klikněte "Register application"

4. **Zkopírujte si Client ID a Client Secret:**
   - Na stránce aplikace uvidíte "Client ID"
   - Klikněte na "Generate a new client secret"
   - **Zkopírujte si Client ID a Client Secret** (Secret se zobrazí pouze jednou!)

### 1.3 Microsoft OAuth2 (Azure AD)

1. **Jděte na Azure Portal:**
   - Otevřete: https://portal.azure.com/
   - Přihlaste se svým Microsoft účtem

2. **Vytvořte App Registration:**
   - V levém menu vyhledejte "Azure Active Directory"
   - V levém menu klikněte na "App registrations"
   - Klikněte na "New registration"

3. **Vyplňte formulář:**
   - **Name:** Maturitní projekt
   - **Supported account types:** Vyberte "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI:**
     - Platform: Web
     - URI: `http://localhost:8000/accounts/microsoft/login/callback/`
   - Klikněte "Register"

4. **Zkopírujte Application (client) ID:**
   - Na stránce "Overview" uvidíte "Application (client) ID" - zkopírujte si ho

5. **Vytvořte Client Secret:**
   - V levém menu klikněte na "Certificates & secrets"
   - Klikněte na "New client secret"
   - Zadejte Description: "Maturitní projekt secret"
   - Expires: Vyberte dobu platnosti (např. 24 months)
   - Klikněte "Add"
   - **Zkopírujte si Value** (Secret se zobrazí pouze jednou!)

---

## KROK 2: Vytvoření .env souboru

1. **Otevřete kořenový adresář projektu** (kde je `manage.py`)

2. **Vytvořte nový soubor `.env`** (nebo otevřete existující)

3. **Přidejte následující řádky** a nahraďte hodnoty těmi, které jste zkopírovali:

```env
# Google OAuth2
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz

# GitHub OAuth2
GITHUB_CLIENT_ID=abcdefghijklmnopqrst
GITHUB_CLIENT_SECRET=1234567890abcdefghijklmnopqrstuvwxyz123456

# Microsoft OAuth2
MICROSOFT_CLIENT_ID=12345678-1234-1234-1234-123456789abc
MICROSOFT_CLIENT_SECRET=abc~1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

**DŮLEŽITÉ:**
- Neodstraňujte uvozovky kolem hodnot
- Každý řádek musí být ve formátu `KLÍČ=hodnota`
- Nezapomeňte uložit soubor

---

## KROK 3: Spuštění migrací

Otevřete terminál v kořenovém adresáři projektu a spusťte:

```bash
# Aktivujte virtuální prostředí (pokud ho používáte)
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Spusťte migrace
python manage.py migrate
```

Tím se vytvoří potřebné tabulky v databázi pro OAuth2.

---

## KROK 4: Vytvoření Social Applications

Spusťte management command, který automaticky vytvoří Social Applications z vašeho `.env` souboru:

```bash
python manage.py create_social_apps
```

Měli byste vidět výstup podobný tomuto:
```
✓ Vytvořena Google Social Application
✓ Vytvořena GitHub Social Application
✓ Vytvořena Microsoft Social Application
Hotovo! Social Applications byly vytvořeny/aktualizovány.
```

**Pokud vidíte varování:**
- `⚠ Google OAuth2 není nakonfigurován` - zkontrolujte, že máte správně nastavené `GOOGLE_CLIENT_ID` a `GOOGLE_CLIENT_SECRET` v `.env`
- Stejně pro GitHub a Microsoft

---

## KROK 5: Testování

1. **Spusťte vývojový server:**
   ```bash
   python manage.py runserver
   ```

2. **Otevřete prohlížeč a jděte na:**
   ```
   http://localhost:8000/accounts/login/
   ```

3. **Měli byste vidět:**
   - Tlačítko "Přihlásit se přes Google"
   - Tlačítko "Přihlásit se přes GitHub"
   - Tlačítko "Přihlásit se přes Microsoft"
   - Formulář pro klasické přihlášení

4. **Otestujte OAuth2:**
   - Klikněte na jedno z OAuth2 tlačítek
   - Měli byste být přesměrováni na přihlášení poskytovatele
   - Po úspěšném přihlášení budete přesměrováni zpět do aplikace
   - Měli byste být automaticky přihlášeni

---

## Řešení problémů

### Tlačítka se nezobrazují

1. **Zkontrolujte, že jsou credentials v .env:**
   ```bash
   # Windows PowerShell
   Get-Content .env
   
   # Linux/Mac
   cat .env
   ```

2. **Zkontrolujte, že byly vytvořeny Social Applications:**
   ```bash
   python manage.py create_social_apps
   ```

3. **Zkontrolujte v Django Admin:**
   - Jděte na `http://localhost:8000/django-admin/`
   - Přihlaste se jako superuser
   - V sekci "Social Accounts" → "Social Applications" by měly být 3 aplikace

### Chyba "Redirect URI mismatch"

- **Google:** Zkontrolujte, že v Google Cloud Console máte správně nastavený Redirect URI:
  ```
  http://localhost:8000/accounts/google/login/callback/
  ```

- **GitHub:** Zkontrolujte, že v GitHub OAuth App máte:
  ```
  http://localhost:8000/accounts/github/login/callback/
  ```

- **Microsoft:** Zkontrolujte, že v Azure Portal máte:
  ```
  http://localhost:8000/accounts/microsoft/login/callback/
  ```

### "Invalid client" nebo podobné chyby

- Zkontrolujte, že jste správně zkopírovali Client ID a Client Secret
- Ujistěte se, že v `.env` souboru nejsou mezery kolem `=`
- Zkontrolujte, že hodnoty nejsou v uvozovkách (pokud nejsou potřeba)

---

## Pro produkci

Když budete nasazovat na produkční server:

1. **Změňte Redirect URIs** u všech poskytovatelů na:
   ```
   https://vasadomena.cz/accounts/{provider}/login/callback/
   ```

2. **Aktualizujte .env** na produkčním serveru s produkčními credentials

3. **Použijte HTTPS** - OAuth2 vyžaduje HTTPS v produkci

4. **Změňte v settings.py:**
   ```python
   ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # místo 'none'
   ```

---

## Shrnutí - Co jste udělali

✅ Vytvořili OAuth2 aplikace u Google, GitHub a Microsoft  
✅ Přidali credentials do `.env` souboru  
✅ Spustili migrace databáze  
✅ Vytvořili Social Applications pomocí `create_social_apps`  
✅ Otestovali OAuth2 přihlášení  

Nyní by měla OAuth2 autentizace fungovat! 🎉

