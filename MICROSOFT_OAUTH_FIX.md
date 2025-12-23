# Oprava Microsoft OAuth - 401 Unauthorized

## Problém
Při přihlášení přes Microsoft dostáváte HTTP 401 při pokusu získat access token. To znamená problém s autentizací.

## Možné příčiny

### 1. Špatný nebo vypršený Client Secret
Microsoft Client Secrets mají **expiraci** (obvykle 6, 12 nebo 24 měsíců). Pokud vypršel, musíte vytvořit nový.

### 2. Špatně zkopírovaný Client Secret
Client Secret může obsahovat speciální znaky, které se špatně kopírují. Zkontrolujte, že je celý secret správně zkopírovaný.

### 3. Špatně nastavený Redirect URI v Azure Portal
Redirect URI musí být přesně stejný jako v Django.

### 4. Špatné nastavení TENANT
TENANT musí být nastavený správně podle typu účtu.

## Řešení krok za krokem

### Krok 1: Zkontrolujte Client Secret v Azure Portal

1. Jděte na: https://portal.azure.com/
2. Najděte vaši **App Registration**
3. Jděte na **"Certificates & secrets"** v levém menu
4. Zkontrolujte, zda váš Client Secret ještě nevypršel:
   - Pokud má **Expires** datum v minulosti → Secret vypršel!
   - Pokud má **Expires** datum v budoucnosti → Secret je platný

### Krok 2: Vytvořte nový Client Secret (pokud vypršel)

1. V sekci **"Certificates & secrets"**
2. Klikněte na **"+ New client secret"**
3. Zadejte popis (např. "Django app")
4. Vyberte expiraci (doporučuji 24 měsíců)
5. Klikněte na **"Add"**
6. **DŮLEŽITÉ:** Okamžitě zkopírujte **Value** (ne ID!) - zobrazí se jen jednou!
7. Aktualizujte `.env` soubor:
   ```
   MICROSOFT_CLIENT_SECRET=nový-secret-hodnota
   ```

### Krok 3: Zkontrolujte Redirect URI v Azure Portal

1. V Azure Portal → vaše App Registration
2. Jděte na **"Authentication"** v levém menu
3. V sekci **"Redirect URIs"** zkontrolujte:
   - ✅ Mělo by být: `http://localhost:8000/accounts/microsoft/login/callback/`
   - ❌ NESMÍ být: `http://127.0.0.1:8000/accounts/microsoft/login/callback/`
   - ❌ NESMÍ být: `http://localhost:8000//accounts/microsoft/login/callback/` (dvojité lomítko)

4. Pokud není správně, přidejte nebo upravte:
   - Klikněte na **"+ Add a platform"** → **"Web"**
   - Zadejte: `http://localhost:8000/accounts/microsoft/login/callback/`
   - Klikněte na **"Configure"**

### Krok 4: Zkontrolujte TENANT nastavení

V Django settings (`maturitni_projekt/settings/base.py`) by mělo být:
```python
'microsoft': {
    'SCOPE': [
        'openid',
        'email',
        'profile',
    ],
    'TENANT': 'common',  # Pro osobní Microsoft účty i organizační
    'APP': {
        'client_id': config('MICROSOFT_CLIENT_ID', default=''),
        'secret': config('MICROSOFT_CLIENT_SECRET', default=''),
        'key': ''
    }
}
```

**TENANT možnosti:**
- `'common'` - Podporuje osobní Microsoft účty i organizační (doporučeno)
- `'organizations'` - Pouze organizační účty
- `'consumers'` - Pouze osobní Microsoft účty
- `'your-tenant-id'` - Konkrétní tenant ID

### Krok 5: Aktualizujte Social Application v Django Admin

1. Restartujte Django server
2. Jděte na: `http://localhost:8000/django-admin/`
3. Přihlaste se jako superuser
4. Jděte na **"Social Accounts"** → **"Social Applications"**
5. Najděte Microsoft aplikaci
6. Zkontrolujte, že **Client ID** a **Secret** odpovídají hodnotám z `.env`
7. Pokud ne, upravte je a uložte

### Krok 6: Zkontrolujte .env soubor

Ujistěte se, že v `.env` souboru jsou správné hodnoty:
```env
MICROSOFT_CLIENT_ID=vaše-client-id-z-azure
MICROSOFT_CLIENT_SECRET=vaše-client-secret-z-azure
```

**Důležité:**
- Žádné mezery kolem `=`
- Žádné uvozovky kolem hodnot (pokud nejsou potřeba)
- Celý Client Secret musí být zkopírovaný (včetně všech znaků)

### Krok 7: Testování

1. Restartujte Django server
2. Zkuste se přihlásit přes Microsoft znovu
3. Mělo by to fungovat

## Pokud stále nefunguje

1. **Zkontrolujte Django logy** - mohou obsahovat více informací o chybě
2. **Zkontrolujte Azure Portal logy**:
   - Azure Portal → vaše App Registration → **"Sign-in logs"**
   - Můžete vidět, proč autentizace selhala
3. **Zkuste vytvořit novou App Registration** v Azure Portal a použít nové credentials

## Časté chyby

### Chyba: "AADSTS7000215: Invalid client secret"
- **Řešení:** Client Secret je špatně zkopírovaný nebo vypršel. Vytvořte nový.

### Chyba: "AADSTS50011: The redirect URI specified in the request does not match"
- **Řešení:** Redirect URI v Azure Portal neodpovídá URL v Django. Zkontrolujte obě místa.

### Chyba: "AADSTS700016: Application not found"
- **Řešení:** Client ID je špatně zkopírovaný nebo aplikace byla smazána.

