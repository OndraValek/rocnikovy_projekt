# Návod: Vytvoření USE CASE diagramu v Draw.io

## Krok 1: Otevření Draw.io
1. Otevřete prohlížeč a přejděte na: **https://app.diagrams.net/**
2. Klikněte na **"Create New Diagram"**
3. Vyberte **"Blank Diagram"** nebo **"UML"** šablonu
4. Klikněte na **"Create"**

## Krok 2: Nastavení šablony
1. V levém panelu klikněte na **"More Shapes"** (nebo ikonu "+" vlevo dole)
2. Zaškrtněte **"UML"** nebo **"UML Use Case"**
3. Klikněte na **"Apply"**

## Krok 3: Vytvoření aktérů (Actors)
1. V levém panelu najděte sekci **"UML"** nebo **"General"**
2. Najděte ikonu **"Actor"** (človíček) nebo použijte **"General" → "Shape" → "Actor"**
3. Přetáhněte **3x Actor** na plátno a umístěte je **vlevo, pod sebou**:
   - **Student** (nahoře)
   - **Teacher** (uprostřed)
   - **Admin** (dole)
4. Dvojklikem na každého aktéra a napište název

## Krok 4: Vytvoření hlavního rámečku
1. V levém panelu najděte **"General" → "Rectangle"**
2. Nakreslete **velký obdélník**, který bude obsahovat všechny balíčky
3. Dvojklikem napište: **"Maturitní projekt - vzdělávací platforma"**
4. Umístěte ho **napravo od aktérů**

## Krok 5: Vytvoření balíčků (Packages)
1. V levém panelu najděte **"General" → "Rectangle"** nebo **"Container"**
2. Vytvořte **6 obdélníků** pro balíčky a umístěte je **vedle sebe** (nebo 2x3):
   - **"Autentizace a autorizace"**
   - **"Předměty a okruhy"**
   - **"Výukové materiály"**
   - **"Testy a kvízy"**
   - **"Diskusní fórum"**
   - **"Administrace"**
3. Dvojklikem na každý obdélník napište název balíčku

## Krok 6: Vytvoření Use Cases (elipsy)
1. V levém panelu najděte **"UML" → "Use Case"** (elipsa) nebo **"General" → "Ellipse"**
2. Pro každý balíček vytvořte elipsy s názvy use cases:

### Autentizace a autorizace (8 use cases):
- Registrace
- Přihlášení
- OAuth2 přihlášení (Google)
- OAuth2 přihlášení (GitHub)
- OAuth2 přihlášení (Microsoft)
- Odhlášení
- Správa profilu
- Správa uživatelů

### Předměty a okruhy (6 use cases):
- Prohlížet seznam předmětů
- Zobrazit detail předmětu
- Prohlížet okruhy předmětu
- Zobrazit detail okruhu
- Spravovat předměty
- Spravovat okruhy

### Výukové materiály (8 use cases):
- Prohlížet materiály
- Zobrazit detail materiálu
- Stáhnout PDF dokument
- Zobrazit video
- Interagovat s H5P obsahem
- Vytvářet materiály
- Upravovat materiály
- Mazat materiály

### Testy a kvízy (8 use cases):
- Prohlížet dostupné testy
- Zobrazit detail testu
- Spustit test (H5P)
- Zobrazit výsledky testu
- Zobrazit historii pokusů
- Vytvářet testy
- Upravovat testy
- Mazat testy

### Diskusní fórum (8 use cases):
- Prohlížet diskusní vlákna
- Zobrazit detail vlákna
- Vytvořit nové vlákno
- Přidat příspěvek
- Upravit vlastní příspěvek
- Smazat vlastní příspěvek
- Připnout/zamykat vlákno
- Moderovat fórum

### Administrace (4 use cases):
- Správa uživatelů a rolí
- Správa celého obsahu
- Zobrazení statistik
- Export dat

3. Umístěte elipsy **uvnitř příslušných balíčků**
4. Dvojklikem na každou elipsu napište název use case

## Krok 7: Vytvoření vztahů (šipky)
1. V levém panelu najděte **"General" → "Arrow"** nebo použijte **"Connector"**
2. Nakreslete šipky od aktérů k use cases podle vztahů:

### Student → use cases:
- UC1, UC2, UC3, UC4 (Předměty a okruhy - pouze prohlížení)
- UC7, UC8, UC9, UC10, UC11 (Výukové materiály - pouze prohlížení)
- UC15, UC16, UC17, UC18, UC19 (Testy a kvízy - pouze prohlížení a řešení)
- UC23, UC24, UC25, UC26, UC27, UC28 (Diskusní fórum - bez moderování)
- UC31, UC32, UC33, UC34, UC35, UC36, UC37 (Autentizace - bez správy uživatelů)

### Teacher → use cases:
- Všechno co Student PLUS:
- UC5, UC6 (Správa předmětů a okruhů)
- UC12, UC13, UC14 (Správa materiálů)
- UC20, UC21, UC22 (Správa testů)
- UC29, UC30 (Moderování fóra)

### Admin → use cases:
- Všechno co Teacher PLUS:
- UC38 (Správa uživatelů)
- UC39, UC40, UC41, UC42 (Administrace)

3. Klikněte na aktéra, pak na use case - Draw.io automaticky vytvoří šipku

## Krok 8: Úprava layoutu
1. **Vyberte všechny prvky** (Ctrl+A nebo Cmd+A)
2. Klikněte pravým tlačítkem → **"Layout" → "Auto Layout"** (pokud je dostupné)
3. Nebo ručně přesuňte balíčky **vedle sebe** místo pod sebou:
   - První řádek: Autentizace, Předměty, Výukové materiály
   - Druhý řádek: Testy, Diskusní fórum, Administrace
4. Upravte velikosti a pozice pro lepší čitelnost

## Krok 9: Export do PNG
1. Klikněte na **"File" → "Export as" → "PNG"**
2. Nastavte:
   - **Zoom**: 200% nebo 300% (pro lepší kvalitu)
   - **Border**: 10px (volitelné)
   - **Transparent background**: podle potřeby
3. Klikněte na **"Export"**
4. Uložte soubor jako: **`use_case_diagram.png`** do složky **`dokumentace/obrazky/`**

## Krok 10: Vložení do LaTeX dokumentace
Po vytvoření obrázku mi dejte vědět a já ho vložím do dokumentace na správné místo (sekce 2.3.2).

## Tipy:
- Použijte **"Snap to Grid"** pro lepší zarovnání
- Použijte **"Align"** a **"Distribute"** pro rovnoměrné rozmístění
- Můžete změnit barvy balíčků pro lepší rozlišení
- Použijte **"Layers"** pro lepší organizaci (aktéři, balíčky, use cases)

