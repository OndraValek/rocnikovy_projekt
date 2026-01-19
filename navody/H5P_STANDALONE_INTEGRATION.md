# H5P Standalone Integration - Kompletní průvodce

## Přehled

Tento projekt nyní podporuje zobrazování H5P obsahu pomocí [h5p-standalone](https://github.com/tunapanda/h5p-standalone) knihovny. Toto řešení umožňuje:

- ✅ Zobrazování H5P obsahu bez nutnosti externího H5P serveru
- ✅ Ukládání výsledků a stavu uživatele do databáze
- ✅ Podpora xAPI událostí pro tracking pokroku
- ✅ Plná kontrola nad frontendem i backendem

## Instalace h5p-standalone

### Krok 1: Stáhnout h5p-standalone

1. Jdi na https://github.com/tunapanda/h5p-standalone/releases
2. Stáhni nejnovější release (např. `h5p-standalone-x.x.x.zip`)
3. Rozbal archiv

### Krok 2: Zkopírovat soubory do projektu

Zkopíruj následující soubory/složky do `static/h5p-player/`:

```
static/
  h5p-player/
    main.bundle.js
    frame.bundle.js
    styles/
      h5p.css
```

**Příklad příkazu:**
```bash
# Po rozbalení h5p-standalone archivu
cp h5p-standalone/dist/main.bundle.js static/h5p-player/
cp h5p-standalone/dist/frame.bundle.js static/h5p-player/
cp -r h5p-standalone/dist/styles static/h5p-player/
```

### Krok 3: Spustit collectstatic

```bash
python manage.py collectstatic
```

## Příprava H5P obsahu

### Krok 1: Získat H5P soubor

H5P soubory (.h5p) můžete získat z:
- H5P.org (po vytvoření obsahu klikněte na "Download")
- Moodle (export H5P obsahu)
- WordPress s H5P pluginem

### Krok 2: Rozbalit H5P soubor

H5P soubory jsou vlastně ZIP archivy. Použijte management command:

```bash
python manage.py extract_h5p path/to/file.h5p --quiz-id 1
```

Nebo bez automatické aktualizace Quiz:

```bash
python manage.py extract_h5p path/to/file.h5p --slug my-quiz-name
```

**Parametry:**
- `h5p_file` - Cesta k .h5p souboru (povinné)
- `--quiz-id` - ID Quiz objektu, který má být aktualizován
- `--slug` - Slug pro pojmenování složky (pokud není --quiz-id)
- `--force` - Přepsat existující složku

**Příklad:**
```bash
python manage.py extract_h5p ~/Downloads/quiz.h5p --quiz-id 1
```

Tento příkaz:
1. Rozbalí H5P soubor do `media/h5p/quiz-1/`
2. Aktualizuje Quiz s ID 1 s `h5p_path = "h5p/quiz-1/"`

### Krok 3: Ověřit strukturu

Po rozbalení by měla být struktura:

```
media/
  h5p/
    quiz-1/
      h5p.json          # Hlavní konfigurační soubor
      content/
        content.json    # Obsah H5P
      libraries/        # H5P knihovny
        ...
```

## Konfigurace Quiz v Django Admin

### Vytvoření/úprava Quiz

1. Jdi do Django Admin → Quizzes → Add Quiz
2. Vyplň základní údaje (název, okruh, atd.)
3. V sekci "H5P obsah":
   - **h5p_path**: Zadej relativní cestu (např. `h5p/quiz-1/`)
   - **h5p_embed_code**: Ponech prázdné (používá se starší způsob)

4. Ulož

## Jak to funguje

### 1. Zobrazení H5P obsahu

Když uživatel otevře test s `h5p_path`:

1. Django view načte Quiz a připraví kontext s cestami k H5P souborům
2. Šablona načte h5p-standalone JavaScript a CSS
3. JavaScript inicializuje H5P player s:
   - Cestou k `h5p.json`
   - API endpointy pro ukládání stavu
   - Informacemi o uživateli

### 2. Ukládání stavu uživatele

H5P player automaticky ukládá stav uživatele každých 5 sekund (nastaveno v `saveFreq`):

- **GET** `/quizzes/api/h5p/userdata/<content_id>/` - Načte uložený stav
- **POST** `/quizzes/api/h5p/userdata/<content_id>/` - Uloží nový stav

Data se ukládají do modelu `H5PUserData`.

### 3. Zpracování xAPI událostí

Když uživatel dokončí H5P aktivitu, H5P pošle xAPI událost:

- **POST** `/quizzes/api/h5p/xapi/` - Přijme xAPI statement

xAPI událost obsahuje:
- Skóre (raw a max)
- Verb (completed, passed, atd.)
- Informace o odpovědích

Tyto informace se ukládají do `QuizAttempt` modelu.

## API Endpointy

### 1. H5P User Data

**GET/POST** `/quizzes/api/h5p/userdata/<content_id>/`

- **GET**: Vrací uložený stav uživatele
- **POST**: Ukládá nový stav uživatele

**Formát odpovědi (GET):**
```json
[
  {
    "state": "...",
    "subContentId": null
  }
]
```

### 2. xAPI Events

**POST** `/quizzes/api/h5p/xapi/`

Přijímá xAPI statement a ukládá výsledky do `QuizAttempt`.

**Formát requestu:**
```json
{
  "statement": {
    "verb": {
      "id": "http://adlnet.gov/expapi/verbs/completed"
    },
    "object": {
      "id": "http://h5p.org/interactive-video"
    },
    "result": {
      "score": {
        "raw": 8,
        "max": 10
      }
    }
  },
  "quiz_id": 1
}
```

## Modely

### Quiz

Přidáno pole:
- `h5p_path` - Relativní cesta k rozbalenému H5P obsahu

### H5PUserData

Nový model pro ukládání stavu uživatele:
- `user` - Uživatel
- `content_id` - ID H5P obsahu
- `data` - JSON data s uloženým stavem
- `updated_at` - Čas poslední aktualizace

## Řešení problémů

### H5P obsah se nenačítá

1. **Zkontroluj cestu k h5p.json:**
   - Otevři Developer Tools (F12)
   - Podívej se na Network tab
   - Zkontroluj, zda se `h5p.json` načítá správně

2. **Zkontroluj strukturu složky:**
   - Měla by obsahovat `h5p.json`, `content/`, `libraries/`

3. **Zkontroluj konzoli prohlížeče:**
   - Může obsahovat chybové hlášky

### Chybějící knihovny

Pokud H5P obsah neobsahuje všechny potřebné knihovny:

1. Stáhni H5P obsah z Moodle nebo WordPress (obsahuje kompletní knihovny)
2. Nebo ručně doplň chybějící knihovny do `libraries/` složky

### API endpointy nefungují

1. **Zkontroluj autentizaci:**
   - Uživatel musí být přihlášen
   - API endpointy vyžadují `IsAuthenticated` permission

2. **Zkontroluj CSRF token:**
   - V JavaScriptu se používá `{{ csrf_token }}`

3. **Zkontroluj URL:**
   - Ověř, že URL v JavaScriptu odpovídají URL patterns

## Migrace z embed kódu na h5p-standalone

Pokud už máte Quiz s `h5p_embed_code`:

1. Stáhni H5P obsah z externího serveru (pokud je to možné)
2. Rozbal ho pomocí `extract_h5p` command
3. Aktualizuj Quiz v Django Admin:
   - Zadej `h5p_path`
   - `h5p_embed_code` může zůstat (pro zpětnou kompatibilitu)

Aplikace automaticky použije `h5p_path`, pokud je nastaven, jinak použije `h5p_embed_code`.

## Další zdroje

- [h5p-standalone GitHub](https://github.com/tunapanda/h5p-standalone)
- [H5P.org](https://h5p.org/)
- [H5P Documentation](https://h5p.org/documentation)
- [xAPI Specification](https://github.com/adlnet/xAPI-Spec)

## Podpora

Pro problémy nebo otázky kontaktujte učitele nebo vytvořte issue v projektu.

