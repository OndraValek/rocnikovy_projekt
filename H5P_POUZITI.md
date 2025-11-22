# H5P Standalone - Jak použít

## ✅ Co už máš hotové:
- h5p-standalone soubory v `static/h5p-player/`
- `collectstatic` spuštěný
- Migrace vytvořená

## 📋 Co teď udělat:

### 1. Spusť migraci (pokud ještě není spuštěná)

```bash
python manage.py migrate
```

### 2. Vytvoř složku pro H5P obsah

```bash
mkdir media\h5p
```

### 3. Získej H5P soubor (.h5p)

H5P soubory můžeš získat z:
- **H5P.org** - po vytvoření obsahu klikni na "Download"
- **Moodle** - export H5P obsahu
- **WordPress** s H5P pluginem

### 4. Rozbal H5P soubor

Použij management command:

```bash
python manage.py extract_h5p cesta/k/souboru.h5p --quiz-id 1
```

**Příklad:**
```bash
python manage.py extract_h5p C:\Users\Ondra\Downloads\muj-test.h5p --quiz-id 1
```

Tento příkaz:
- Rozbalí H5P soubor do `media/h5p/quiz-1/`
- Automaticky aktualizuje Quiz s ID 1 s `h5p_path = "h5p/quiz-1/"`

**Nebo bez automatické aktualizace:**
```bash
python manage.py extract_h5p cesta/k/souboru.h5p --slug nazev-testu
```

### 5. Nastav Quiz v Django Admin

1. Jdi do **Django Admin** → **Quizzes**
2. Otevři nebo vytvoř Quiz
3. V sekci **"H5P obsah"**:
   - **h5p_path**: Zadej relativní cestu (např. `h5p/quiz-1/`)
     - Pokud jsi použil `--quiz-id`, mělo by to být už nastavené
   - **h5p_embed_code**: Ponech prázdné (používá se jen starší způsob)
4. Ulož

### 6. Otestuj

1. Spusť Django server:
   ```bash
   python manage.py runserver
   ```

2. Otevři test v prohlížeči:
   - Jdi na stránku testu (např. `/quiz/1/attempt/`)
   - Měl by se zobrazit H5P obsah pomocí h5p-standalone

3. Zkontroluj Developer Tools (F12):
   - **Console** - měly by tam být logy o načítání H5P
   - **Network** - zkontroluj, zda se načítají soubory (h5p.json, knihovny)

## 🔍 Řešení problémů

### H5P se nenačítá

1. **Zkontroluj cestu k h5p.json:**
   - Měla by být: `media/h5p/quiz-1/h5p.json`
   - Otevři Developer Tools → Network tab
   - Zkontroluj, zda se `h5p.json` načítá (mělo by být 200 OK)

2. **Zkontroluj strukturu složky:**
   ```
   media/
     h5p/
       quiz-1/
         ├── h5p.json          ← musí existovat
         ├── content/
         │   └── content.json
         └── libraries/         ← musí obsahovat knihovny
   ```

3. **Zkontroluj konzoli prohlížeče:**
   - Může obsahovat chybové hlášky
   - Hledej chyby typu "Cannot load h5p.json" nebo "Library not found"

### Chybějící knihovny

Pokud H5P obsah neobsahuje všechny potřebné knihovny:
- Stáhni H5P obsah z Moodle nebo WordPress (obsahuje kompletní knihovny)
- Nebo ručně doplň chybějící knihovny do `libraries/` složky

### API endpointy nefungují

1. **Zkontroluj autentizaci:**
   - Uživatel musí být přihlášen
   - API endpointy vyžadují přihlášení

2. **Zkontroluj URL:**
   - V Developer Tools → Network tab
   - Zkontroluj, zda se API volání odesílají správně

## 📝 Příklad workflow

1. **Vytvoř H5P obsah** na H5P.org nebo v Moodle
2. **Stáhni .h5p soubor**
3. **Rozbal ho:**
   ```bash
   python manage.py extract_h5p test.h5p --quiz-id 1
   ```
4. **V Django Admin** zkontroluj, že Quiz má správný `h5p_path`
5. **Otevři test** v prohlížeči a vyzkoušej

## 🎯 Co by mělo fungovat

- ✅ H5P obsah se zobrazí na stránce testu
- ✅ Stav uživatele se ukládá automaticky každých 5 sekund
- ✅ Po dokončení testu se výsledky uloží do `QuizAttempt`
- ✅ Skóre se zobrazí po dokončení

## 📚 Více informací

- `docs/H5P_STANDALONE_INTEGRATION.md` - Kompletní dokumentace
- `H5P_STANDALONE_SETUP.md` - Rychlý start



