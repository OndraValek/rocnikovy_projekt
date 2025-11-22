# H5P Integrace - Kompletní průvodce

> **⚠️ DŮLEŽITÉ:** Tento dokument popisuje starší způsob integrace pomocí embed kódu. 
> Pro novou integraci pomocí **h5p-standalone** (doporučeno) viz [H5P_STANDALONE_INTEGRATION.md](./H5P_STANDALONE_INTEGRATION.md)

## Co je H5P?

H5P (HTML5 Package) je open-source nástroj pro vytváření interaktivního vzdělávacího obsahu. Umožňuje vytvářet interaktivní videa, kvízy, prezentace a další vzdělávací aktivity bez programování.

## Jak H5P funguje v projektu

### 1. Základní integrace (starší způsob - embed kód)

H5P obsah se vkládá pomocí **embed kódu** (iframe). To znamená:
- Vytvoříš H5P obsah na externím serveru (např. H5P.org)
- Zkopíruješ embed kód
- Vložíš ho do Django aplikace
- Obsah se zobrazí přímo na stránce

**⚠️ Poznámka:** Tento způsob má omezení - nelze snadno ukládat výsledky a stav uživatele. Pro plnou funkcionalitu použijte [h5p-standalone integraci](./H5P_STANDALONE_INTEGRATION.md).

### 2. Kde lze použít H5P

#### A) Materiály (Materials)
- V Django Admin → Materials
- Vyber typ: "H5P interaktivní obsah"
- Vlož embed kód do pole "H5P embed kód"

#### B) Testy (Quizzes)
- V Django Admin → Quizzes
- Vlož embed kód do pole "H5P embed kód"
- Test se zobrazí na stránce testu

#### C) Wagtail stránky okruhů
- V Wagtail Admin → Topic Pages
- Přidej H5P blok do StreamField
- Vlož embed kód

## Jak získat H5P embed kód

### Možnost 1: H5P.org (zdarma, veřejné)

1. Jdi na https://h5p.org/
2. Vytvoř účet (nebo se přihlas)
3. Vytvoř nový H5P obsah
4. Po vytvoření klikni na "Embed"
5. Zkopíruj iframe kód
6. Vlož ho do Django aplikace

**Příklad embed kódu:**
```html
<iframe src="https://h5p.org/h5p/embed/123" width="800" height="600" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
```

### Možnost 2: Vlastní H5P server (pokročilé)

Pokud chceš mít vlastní H5P server:
1. Nainstaluj H5P server (WordPress plugin nebo standalone)
2. Vytvářej obsah na vlastním serveru
3. Používej embed kódy z vlastního serveru

## Implementace v projektu

### Aktuální stav

✅ **Co už funguje:**
- Pole pro H5P embed kód v modelech
- Zobrazení H5P obsahu v šablonách
- Podpora v materiálech a testech

❌ **Co chybí:**
- Automatické ukládání výsledků z H5P testů
- JavaScript pro komunikaci s H5P
- API endpoint pro zpracování výsledků
- Zobrazení výsledků v QuizAttempt

### Co by bylo dobré přidat

1. **JavaScript pro zachycení výsledků**
   - H5P posílá výsledky přes postMessage API
   - Potřebujeme JavaScript listener

2. **API endpoint pro ukládání výsledků**
   - Endpoint pro přijetí výsledků z H5P
   - Uložení do QuizAttempt modelu

3. **Vylepšené šablony**
   - JavaScript pro komunikaci s H5P
   - Zobrazení výsledků po dokončení

## Jak použít H5P teď (základní způsob)

### Krok 1: Vytvoř H5P obsah

1. Jdi na https://h5p.org/
2. Přihlas se nebo vytvoř účet
3. Klikni na "Create new content"
4. Vyber typ obsahu (např. "Quiz", "Interactive Video")
5. Vytvoř obsah
6. Ulož a publikuj

### Krok 2: Zkopíruj embed kód

1. Po vytvoření klikni na "Embed"
2. Zkopíruj celý iframe kód
3. Příklad:
```html
<iframe src="https://h5p.org/h5p/embed/123" width="800" height="600" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
```

### Krok 3: Vlož do Django

#### Pro materiál:
1. Django Admin → Materials → Add Material
2. Vyplň základní údaje
3. Typ: "H5P interaktivní obsah"
4. Vlož embed kód do "H5P embed kód"
5. Ulož

#### Pro test:
1. Django Admin → Quizzes → Add Quiz
2. Vyplň základní údaje
3. Vlož embed kód do "H5P embed kód"
4. Nastav časový limit, max pokusy, passing score
5. Ulož

### Krok 4: Zobraz na stránce

- Materiál: `/subjects/<subject>/<topic>/materials/<material_id>/`
- Test: `/subjects/<subject>/<topic>/quizzes/<quiz_id>/attempt/`

## Budoucí vylepšení

### 1. Automatické ukládání výsledků

Přidat JavaScript, který:
- Naslouchá na H5P postMessage události
- Získává výsledky (skóre, čas, odpovědi)
- Posílá je na Django API endpoint
- Ukládá do QuizAttempt

### 2. Zobrazení výsledků

- Zobrazit skóre po dokončení testu
- Zobrazit historii pokusů
- Zobrazit statistiky pro učitele

### 3. Vlastní H5P server (volitelné)

- Nainstalovat vlastní H5P server
- Vytvářet obsah přímo v aplikaci
- Lepší kontrola nad obsahem

## Tipy a triky

1. **Responzivní design**: H5P iframe má fixní šířku/výšku. Můžeš použít CSS pro responzivní zobrazení:
```css
.h5p-container {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 */
    height: 0;
    overflow: hidden;
}
.h5p-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
```

2. **Bezpečnost**: Používej `|safe` filter opatrně - H5P embed kód by měl být důvěryhodný

3. **Výkon**: H5P obsah se načítá z externího serveru, může to zpomalit načítání stránky

## Zdroje

- [H5P.org](https://h5p.org/) - Vytváření H5P obsahu
- [H5P Documentation](https://h5p.org/documentation) - Dokumentace
- [H5P Content Types](https://h5p.org/content-types-and-applications) - Typy obsahu

