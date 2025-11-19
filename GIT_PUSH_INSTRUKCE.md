# Instrukce pro push na GitHub

Kvůli problémům s PowerShell, prosím spusť tyto příkazy **ručně v terminálu** (Git Bash, CMD, nebo PowerShell):

## Příkazy pro push:

```bash
# 1. Přidat všechny změny
git add quizzes/
git add templates/
git add docs/
git add static/
git add *.md
git add quizzes/management/

# 2. Commit s popisem
git commit -m "Přidána integrace h5p-standalone pro H5P moduly

- Přidáno pole h5p_path do modelu Quiz
- Vytvořen model H5PUserData pro ukládání stavu uživatele
- Přidány API endpointy pro h5p-standalone (userdata, xAPI)
- Upraveny views a šablony pro podporu h5p-standalone
- Vytvořen management command extract_h5p pro rozbalení H5P souborů
- Přidána dokumentace pro h5p-standalone integraci
- Podpora pro zpětnou kompatibilitu s h5p_embed_code"

# 3. Push na GitHub
git push origin master
```

## Nebo použij Git Bash / CMD:

1. Otevři **Git Bash** nebo **CMD**
2. Přejdi do adresáře projektu:
   ```bash
   cd "C:\Users\Ondra\OneDrive\Plocha\škola\Ondra škola\Střední škola\PVY\maturitni_projekt_druhy_pokus"
   ```
3. Spusť příkazy výše

## Nebo použij Git GUI:

1. Otevři **Git GUI** nebo **GitHub Desktop**
2. Přidej všechny změny
3. Napiš commit message (viz výše)
4. Klikni na **Push**

## Co se pushne:

- ✅ `quizzes/models.py` - nové modely
- ✅ `quizzes/admin.py` - aktualizovaný admin
- ✅ `quizzes/api_views.py` - nové API endpointy
- ✅ `quizzes/urls.py` - nové URL patterns
- ✅ `quizzes/views.py` - upravené views
- ✅ `quizzes/management/commands/extract_h5p.py` - nový command
- ✅ `templates/quizzes/quiz_attempt.html` - upravená šablona
- ✅ `docs/H5P_STANDALONE_INTEGRATION.md` - nová dokumentace
- ✅ `docs/H5P_INTEGRATION.md` - aktualizovaná dokumentace
- ✅ Všechny nové .md soubory (H5P_POUZITI.md, atd.)
- ✅ `static/h5p-player/README.md` - instrukce pro h5p-player
- ✅ Migrace `quizzes/migrations/0003_*.py`

