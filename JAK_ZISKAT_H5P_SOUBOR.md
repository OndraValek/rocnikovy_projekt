# Jak získat H5P soubor (.h5p)

## Možnost 1: Vytvořit nový H5P obsah na H5P.org (doporučeno pro začátek)

### Krok 1: Vytvoř účet na H5P.org
1. Jdi na https://h5p.org/
2. Klikni na **"Sign up"** (vpravo nahoře)
3. Vytvoř si účet (můžeš použít email nebo se přihlásit přes Google/GitHub)

### Krok 2: Vytvoř H5P obsah
1. Po přihlášení klikni na **"Create"** (nebo "Create new content")
2. Vyber typ H5P obsahu, který chceš vytvořit:

   **Pro testy/kvízy doporučuji:**
   - **Quiz** - jednoduchý kvíz s otázkami
   - **Interactive Video** - video s otázkami
   - **Question Set** - sada otázek
   - **Multiple Choice** - výběr z možností
   - **True/False Question** - ano/ne otázky
   - **Fill in the Blanks** - doplňování
   - **Drag and Drop** - přetahování
   - **Single Choice Set** - výběr jedné možnosti

3. Vyplň obsah:
   - Přidej otázky
   - Nastav správné odpovědi
   - Přidej popisky, obrázky, atd.

4. Klikni na **"Save"** (nebo "Create")

### Krok 3: Stáhni H5P soubor
1. Po uložení obsahu uvidíš náhled
2. Klikni na tlačítko **"Download"** (nebo ikonu stahování)
3. Stáhne se soubor s příponou `.h5p` (např. `my-quiz.h5p`)

**Poznámka:** Pokud nevidíš tlačítko "Download", můžeš:
- Kliknout na tři tečky (⋮) vedle obsahu
- Vybrat "Download" z menu

---

## Možnost 2: Použít existující H5P obsah z H5P.org

1. Jdi na https://h5p.org/content
2. Procházej dostupný obsah
3. Klikni na obsah, který se ti líbí
4. Pokud máš oprávnění, můžeš ho stáhnout

**Poznámka:** Ne všechny obsahy na H5P.org jsou ke stažení (záleží na autorovi).

---

## Možnost 3: Export z Moodle (pokud máš přístup)

1. Přihlas se do Moodle
2. Jdi do kurzu s H5P obsahem
3. Otevři H5P aktivitu
4. Klikni na **"Download"** nebo **"Export"**
5. Stáhne se `.h5p` soubor

---

## Možnost 4: Export z WordPress (pokud máš WordPress s H5P pluginem)

1. Přihlas se do WordPress adminu
2. Jdi do **H5P Content** → **All Content**
3. Klikni na H5P obsah
4. Klikni na **"Download"** nebo **"Export"**

---

## Co stáhnout?

Stáhni **celý H5P soubor** s příponou `.h5p` - to je ZIP archiv, který obsahuje:
- Konfiguraci (`h5p.json`)
- Obsah (`content/content.json`)
- Všechny potřebné knihovny (`libraries/`)

**Nestahuj:**
- ❌ Embed kód (iframe)
- ❌ Jen obrázky nebo videa
- ❌ HTML soubory

**Stáhni:**
- ✅ Soubor s příponou `.h5p` (např. `my-quiz.h5p`)

---

## Rychlý test - vytvoř jednoduchý kvíz

Pokud chceš rychle vyzkoušet, můžeš vytvořit jednoduchý test:

1. Jdi na https://h5p.org/
2. Přihlas se
3. Klikni na **"Create"**
4. Vyber **"Quiz"** nebo **"Question Set"**
5. Přidej 2-3 jednoduché otázky (např. "Jaká je hlavní město ČR?" → "Praha")
6. Ulož
7. Stáhni `.h5p` soubor
8. Použij ho v projektu pomocí:
   ```bash
   python manage.py extract_h5p stazeny-soubor.h5p --quiz-id 1
   ```

---

## Tipy

- **Pro testování:** Začni s jednoduchým kvízem (2-3 otázky)
- **Pro produkci:** Vytvoř kompletní testy s více otázkami
- **Velikost souboru:** H5P soubory jsou obvykle malé (několik MB), pokud neobsahují velká videa
- **Kontrola:** Po stažení zkontroluj, že soubor má příponu `.h5p` a není prázdný

---

## Co dál?

Po stažení H5P souboru:
1. Rozbal ho pomocí: `python manage.py extract_h5p soubor.h5p --quiz-id 1`
2. Nastav Quiz v Django Admin
3. Otestuj v prohlížeči

Více info v `H5P_POUZITI.md`


