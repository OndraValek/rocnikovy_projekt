# Nastavení Microsoft OAuth - Krok za krokem

## Problém 1: Azure Portal - Redirect URI chyba

Na první fotce vidíte chybu v Azure Portal. Azure Portal někdy vyžaduje HTTPS, ale pro localhost to není nutné.

**Řešení:**
1. V Azure Portal → vaše App Registration → "Authentication"
2. V sekci "Redirect URIs" zkontrolujte, že máte správně nastavené:
   - Platform: **Web**
   - URL: `http://localhost:8000/accounts/microsoft/login/callback/`
3. Pokud stále píše chybu, zkuste:
   - Odstranit URL a přidat ji znovu
   - Nebo použít: `http://127.0.0.1:8000/accounts/microsoft/login/callback/` (ale pak musíte použít 127.0.0.1 i v Django)

## Problém 2: Který Secret použít?

Na druhé fotce vidíte tabulku s Client Secrets. 

**DŮLEŽITÉ:**
- V Django Admin potřebujete **Value** (hodnotu secretu), ne **Secret ID**!
- Na fotce vidíte Value: `9aq******************` (částečně skryté)
- Secret ID: `59b43981-0acc-403e-931d-eb33ef278958` - to NEPOUŽÍVEJTE!

**Jak získat celou hodnotu Value:**
1. V Azure Portal → vaše App Registration → "Certificates & secrets"
2. Najděte váš secret (ten s expirací 11/15/2027)
3. Klikněte na ikonu **kopírování** vedle sloupce "Value"
4. Zkopírujte celou hodnotu (začíná na `9aq...`)

**Pokud už nemůžete vidět Value:**
- Microsoft zobrazuje Value jen jednou při vytvoření
- Pokud jste ho nezkopírovali, musíte vytvořit **nový secret**:
  1. Klikněte na "+ New client secret"
  2. Zadejte popis
  3. Vyberte expiraci
  4. Klikněte "Add"
  5. **OKAMŽITĚ zkopírujte Value** - zobrazí se jen jednou!

## Problém 3: Co dát do pole "Klíč" v Django Admin?

Na třetí fotce vidíte Django Admin formulář. 

**Co máte opravit:**

1. **"Tajný klíč" (Secret key):**
   - ❌ ŠPATNĚ: `59b43981-0acc-403e-931d-eb33ef278958` (to je Secret ID!)
   - ✅ SPRÁVNĚ: `9aq...` (celá hodnota Value z Azure Portal)
   - Vložte tam **celou hodnotu Value** z Azure Portal (začíná na `9aq...`)

2. **"Klíč" (Key):**
   - ✅ Může zůstat **PRÁZDNÉ** pro Microsoft OAuth
   - Toto pole se používá jen pro některé poskytovatele (např. Twitter)
   - Pro Microsoft ho nechte prázdné

3. **"Id klienta" (Client ID):**
   - ✅ Správně: `a6540deb-3ac4-4002-8eab-cf899e37dcc2`
   - To je v pořádku

4. **"Sites":**
   - ✅ Správně: `localhost:8000` je vybraný
   - To je v pořádku

## Postup opravy v Django Admin:

1. Jděte na: `http://localhost:8000/django-admin/`
2. Přihlaste se jako superuser
3. Jděte na "Social Accounts" → "Social Applications"
4. Klikněte na Microsoft aplikaci
5. V poli **"Tajný klíč"**:
   - Vymažte současnou hodnotu (`59b43981-0acc-403e-931d-eb33ef278958`)
   - Vložte **celou hodnotu Value** z Azure Portal (začíná na `9aq...`)
6. Pole **"Klíč"** nechte prázdné
7. Klikněte na **"ULOŽIT"**

## Pokud nemáte Value secretu:

Musíte vytvořit nový secret v Azure Portal:

1. Azure Portal → vaše App Registration → "Certificates & secrets"
2. Klikněte na "+ New client secret"
3. Zadejte popis (např. "Django app")
4. Vyberte expiraci (doporučuji 24 měsíců)
5. Klikněte "Add"
6. **OKAMŽITĚ zkopírujte Value** (zobrazí se jen jednou!)
7. Vložte ho do Django Admin → "Tajný klíč"
8. Aktualizujte také `.env` soubor:
   ```
   MICROSOFT_CLIENT_SECRET=nová-hodnota-value
   ```

## Shrnutí:

- ✅ **Client ID**: `a6540deb-3ac4-4002-8eab-cf899e37dcc2` (správně)
- ❌ **Secret key**: `59b43981-0acc-403e-931d-eb33ef278958` (špatně - to je Secret ID!)
- ✅ **Secret key**: `9aq...` (celá hodnota Value z Azure Portal)
- ✅ **Key**: prázdné (správně)
- ✅ **Sites**: `localhost:8000` (správně)

