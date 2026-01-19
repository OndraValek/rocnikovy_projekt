# H5P Standalone - Rychlý start

## Co bylo implementováno

✅ **Modely:**
- Přidáno pole `h5p_path` do modelu `Quiz`
- Vytvořen model `H5PUserData` pro ukládání stavu uživatele

✅ **API Endpointy:**
- `/quizzes/api/h5p/userdata/<content_id>/` - GET/POST pro ukládání stavu
- `/quizzes/api/h5p/xapi/` - POST pro xAPI události

✅ **Views a šablony:**
- Upravena `QuizAttemptView` pro podporu h5p-standalone
- Upravena šablona `quiz_attempt.html` s JavaScriptem pro h5p-standalone

✅ **Management command:**
- `python manage.py extract_h5p` - pro rozbalení H5P souborů

## Co je potřeba udělat

### 1. Vytvořit migraci

```bash
python manage.py makemigrations quizzes
python manage.py migrate
```

### 2. Stáhnout a nainstalovat h5p-standalone

1. Jdi na https://github.com/tunapanda/h5p-standalone/releases
2. Stáhni nejnovější release
3. Rozbal a zkopíruj do `static/h5p-player/`:
   - `main.bundle.js`
   - `frame.bundle.js`
   - `styles/h5p.css`

### 3. Spustit collectstatic

```bash
python manage.py collectstatic
```

### 4. Vytvořit složku pro H5P obsah

```bash
mkdir -p media/h5p
```

## Použití

### Rozbalení H5P souboru

```bash
python manage.py extract_h5p path/to/file.h5p --quiz-id 1
```

### Nastavení v Django Admin

1. Jdi do Quizzes → Add/Edit Quiz
2. V poli "h5p_path" zadej: `h5p/quiz-1/` (nebo jinou cestu)
3. Ulož

## Dokumentace

Více informací najdeš v:
- `docs/H5P_STANDALONE_INTEGRATION.md` - Kompletní průvodce
- `docs/H5P_INTEGRATION.md` - Starší dokumentace (embed kód)

## Testování

1. Vytvoř Quiz s `h5p_path`
2. Otevři test v prohlížeči
3. Zkontroluj Developer Tools (F12) pro případné chyby
4. Vyplň test a zkontroluj, zda se výsledky ukládají

