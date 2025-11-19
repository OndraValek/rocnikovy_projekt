# Alternativní způsoby stažení H5P souboru

## Problém: V menu není "Download"

Pokud v menu tří teček (⋮) není možnost "Download", zkus tyto alternativy:

---

## Metoda 1: Přes Editor (ikona tužky) - nejpravděpodobnější

1. **Klikni na ikonu tužky** (modrý čtverec s bílou tužkou) vedle H5P obsahu
2. Otevře se editor H5P obsahu
3. V editoru hledej:
   - Tlačítko **"Download"** v horní liště
   - Nebo menu **"File"** → **"Download"** / **"Export"**
   - Nebo ikonu **stahování** (šipka dolů)
   - Nebo tři tečky (⋮) v editoru → "Download"

---

## Metoda 2: Přes "Clone" a pak stáhnout

1. V menu tří teček klikni na **"Clone"**
2. Vytvoří se kopie obsahu
3. U kopie zkus najít možnost stahování (možná je dostupná u vlastního obsahu)

---

## Metoda 3: Zkontroluj, zda nejsi na H5P.com (místo H5P.org)

**H5P.com** (komerční platforma) může mít jiné možnosti než **H5P.org** (open source).

### Pokud jsi na H5P.com:
- Možná potřebuješ **premium účet** pro stahování
- Nebo stahování není dostupné na této platformě
- Zkus se podívat do **nastavení účtu** nebo **subscription**

### Pokud jsi na H5P.org:
- Stahování by mělo být dostupné
- Zkus se přihlásit na **H5P.org** místo H5P.com

---

## Metoda 4: Použij H5P.org místo H5P.com

1. Jdi na **https://h5p.org/** (ne H5P.com)
2. Přihlas se nebo vytvoř účet
3. Vytvoř nový H5P obsah nebo importuj existující
4. Na H5P.org by mělo být tlačítko "Download" dostupné

---

## Metoda 5: Export přes API (pokročilé)

Pokud máš přístup k API nebo máš technické znalosti:
- H5P obsah může být dostupný přes API endpoint
- Ale to je složitější a vyžaduje technické znalosti

---

## Metoda 6: Vytvoř nový obsah na H5P.org

Pokud stahování není dostupné na současné platformě:

1. Jdi na **https://h5p.org/**
2. Vytvoř si účet (zdarma)
3. Vytvoř nový H5P obsah:
   - Klikni na **"Create"**
   - Vyber typ (Quiz, Question Set, atd.)
   - Vytvoř obsah (můžeš zkopírovat otázky z existujícího obsahu)
4. Ulož a stáhni (na H5P.org by mělo být tlačítko "Download")

---

## Metoda 7: Použij embed kód (dočasné řešení)

Pokud nemůžeš stáhnout `.h5p` soubor:

1. V menu tří teček nebo v editoru hledej **"Embed"** nebo **"Share"**
2. Zkopíruj **embed kód** (iframe)
3. V Django projektu použij **starší způsob** s `h5p_embed_code`:
   - V Django Admin → Quiz → pole "h5p_embed_code"
   - Vlož embed kód
   - **Poznámka:** Tento způsob má omezení - nelze ukládat výsledky tak dobře

---

## Co zkusit teď:

### Krok 1: Zkus Editor
1. Klikni na **ikonu tužky** (edit) u některého H5P obsahu
2. V editoru hledej možnost stahování

### Krok 2: Zkontroluj platformu
- Jsi na **H5P.com** nebo **H5P.org**?
- Pokud na H5P.com, zkus přejít na H5P.org

### Krok 3: Vytvoř nový obsah
- Pokud stahování není dostupné, vytvoř nový obsah na H5P.org
- Tam by mělo být stahování dostupné

---

## Rychlé řešení pro testování:

Pokud potřebuješ rychle otestovat integraci:

1. Jdi na **https://h5p.org/**
2. Vytvoř si účet (zdarma)
3. Vytvoř jednoduchý test:
   - "Create" → "Quiz" nebo "Question Set"
   - Přidej 2-3 otázky
   - Ulož
4. Stáhni `.h5p` soubor (na H5P.org by mělo být tlačítko "Download")
5. Použij v projektu:
   ```bash
   python manage.py extract_h5p stazeny-soubor.h5p --quiz-id 1
   ```

---

## Tip:

Pokud máš obsah na **H5P.com** a nemůžeš ho stáhnout, můžeš:
- Zkopírovat otázky a vytvořit nový obsah na **H5P.org**
- Nebo použít embed kód (ale s omezeními)


