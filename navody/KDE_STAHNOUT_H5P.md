# Kde stáhnout H5P soubor na H5P.com

## Metoda 1: Přes menu tří teček (⋮) - nejjednodušší

1. **Najdi H5P obsah**, který chceš stáhnout (např. "Základy informatiky - Question Set")
2. **Klikni na tři tečky (⋮)** na pravém konci řádku (vedle ikony tužky)
3. V rozbalovacím menu by mělo být:
   - **"Download"** nebo **"Export"** nebo **"Download as .h5p"**
4. Klikni na to → stáhne se soubor `.h5p`

## Metoda 2: Po otevření obsahu

1. **Klikni na název H5P obsahu** (např. "Základy informatiky - Question Set")
2. Otevře se náhled/editor
3. V horní liště nebo v menu hledej:
   - **"Download"** tlačítko
   - Nebo ikonu stahování (šipka dolů)
   - Nebo tři tečky (⋮) → "Download"

## Metoda 3: Přes "Smart Import" (hromadné stahování)

1. **Zaškrtni checkboxy** u H5P obsahů, které chceš stáhnout
2. V horní liště klikni na **"Smart Import"** (modré tlačítko s ikonou stahování)
3. Nebo použij akce pro vybrané položky

## Metoda 4: Přes ikonu tužky (Edit)

1. **Klikni na ikonu tužky** (edit) vedle H5P obsahu
2. Otevře se editor
3. V editoru hledej tlačítko **"Download"** nebo **"Export"**

## Co hledat:

- ✅ Tlačítko **"Download"**
- ✅ Ikona **stahování** (šipka dolů ⬇️)
- ✅ **"Export"** nebo **"Export as .h5p"**
- ✅ Menu **tři tečky (⋮)** → "Download"

## Co stáhnout:

- ✅ Soubor s příponou **`.h5p`** (např. `zaklady-informatiky-question-set.h5p`)
- ❌ NESTAHUJ: Embed kód, HTML, nebo jen obrázky

## Tip:

Pokud nevidíš tlačítko "Download":
- Zkontroluj, zda máš oprávnění ke stažení (některé obsahy mohou být chráněné)
- Zkus kliknout přímo na název obsahu a hledat v detailu
- Zkontroluj, zda nejsi v módu "View" - přepni na "Edit" nebo "Manage"

## Po stažení:

1. Ulož soubor `.h5p` na disk (např. do složky Downloads)
2. Použij v projektu:
   ```bash
   python manage.py extract_h5p cesta/k/souboru.h5p --quiz-id 1
   ```


