# Oprava Microsoft OAuth - 403 Forbidden při získávání dat

## Problém

Z logů vidím:
- ✅ Token byl úspěšně získán: `200 OK`
- ❌ Microsoft Graph API vrací `403 Forbidden` při pokusu získat uživatelská data

To znamená, že aplikace **nemá správná oprávnění** v Azure Portal.

## Řešení - Nastavení API Permissions v Azure Portal

### Krok 1: Přidání Microsoft Graph API Permissions

1. Jděte na: https://portal.azure.com/
2. Najděte vaši **App Registration**
3. V levém menu klikněte na **"API permissions"** (nebo "Oprávnění rozhraní API")
4. Klikněte na **"+ Add a permission"**
5. Vyberte **"Microsoft Graph"**
6. Vyberte **"Delegated permissions"** (ne Application permissions)

### Krok 2: Přidání potřebných oprávnění

Přidejte následující oprávnění (zaškrtněte je):

**Základní oprávnění:**
- ✅ `openid` - Sign users in
- ✅ `email` - View users' email address
- ✅ `profile` - View users' basic profile

**Další potřebná oprávnění:**
- ✅ `User.Read` - Sign in and read user profile
- ✅ `offline_access` - Maintain access to data you have given it access to

**Jak přidat:**
1. V sekci "Delegated permissions" vyhledejte každé oprávnění
2. Zaškrtněte je
3. Klikněte na **"Add permissions"**

### Krok 3: Admin Consent (pokud je potřeba)

Některá oprávnění mohou vyžadovat **Admin Consent**:
- Pokud vidíte vedle oprávnění tlačítko **"Grant admin consent"**, klikněte na něj
- Nebo požádejte administrátora, aby udělil souhlas

### Krok 4: Zkontrolujte nastavení v Django

V Django settings (`maturitni_projekt/settings/base.py`) by mělo být:

```python
'microsoft': {
    'SCOPE': [
        'openid',
        'email',
        'profile',
        'User.Read',  # Přidat toto!
        'offline_access',  # Přidat toto!
    ],
    'TENANT': 'common',
    'APP': {
        'client_id': config('MICROSOFT_CLIENT_ID', default=''),
        'secret': config('MICROSOFT_CLIENT_SECRET', default=''),
        'key': ''
    }
}
```

### Krok 5: Restart Django serveru

Po změnách restartujte Django server:
```bash
# Zastavte server (CTRL+C)
# Spusťte znovu
python manage.py runserver
```

## Alternativní řešení - Použít jiné scopes

Pokud stále nefunguje, zkuste použít minimální scopes:

```python
'microsoft': {
    'SCOPE': [
        'openid',
        'email',
        'profile',
    ],
    'TENANT': 'common',
    'APP': {
        'client_id': config('MICROSOFT_CLIENT_ID', default=''),
        'secret': config('MICROSOFT_CLIENT_SECRET', default=''),
        'key': ''
    }
}
```

A v Azure Portal přidejte pouze:
- `openid`
- `email`
- `profile`
- `User.Read`

## Kontrola v Azure Portal

Po přidání oprávnění byste měli vidět v Azure Portal → vaše App Registration → "API permissions":

- ✅ Microsoft Graph
  - ✅ openid (Delegated)
  - ✅ email (Delegated)
  - ✅ profile (Delegated)
  - ✅ User.Read (Delegated)
  - ✅ offline_access (Delegated)

## Testování

1. Restartujte Django server
2. Zkuste se přihlásit přes Microsoft znovu
3. Mělo by to fungovat bez 403 chyby

## Pokud stále nefunguje

1. **Zkontrolujte Azure Portal → vaše App Registration → "Sign-in logs"**:
   - Můžete vidět detailní informace o chybě
   - Zkontrolujte, zda jsou oprávnění správně udělena

2. **Zkontrolujte, zda je Admin Consent udělen**:
   - Některá oprávnění vyžadují souhlas administrátora
   - V Azure Portal → "API permissions" → klikněte na "Grant admin consent"

3. **Zkuste vytvořit novou App Registration**:
   - Někdy pomůže začít od začátku s novou aplikací

