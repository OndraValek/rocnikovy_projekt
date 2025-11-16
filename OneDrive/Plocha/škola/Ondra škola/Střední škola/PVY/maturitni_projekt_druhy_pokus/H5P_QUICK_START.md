# H5P - Rychlý start

## Co je implementováno

✅ **Základní integrace:**
- Pole pro H5P embed kód v materiálech a testech
- Zobrazení H5P obsahu na stránkách
- Responzivní zobrazení

✅ **Pokročilá integrace:**
- JavaScript pro zachycení výsledků z H5P
- API endpoint pro ukládání výsledků
- Automatické ukládání skóre do QuizAttempt

## Jak použít H5P

### 1. Vytvoř H5P obsah

1. Jdi na https://h5p.org/
2. Vytvoř účet (zdarma)
3. Klikni "Create new content"
4. Vyber typ (např. "Quiz", "Interactive Video")
5. Vytvoř obsah
6. Ulož a publikuj

### 2. Zkopíruj embed kód

1. Po vytvoření klikni na "Embed"
2. Zkopíruj celý iframe kód
3. Příklad:
```html
<iframe src="https://h5p.org/h5p/embed/123" width="800" height="600" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
```

### 3. Vlož do Django

#### Pro materiál:
1. Django Admin → Materials → Add Material
2. Typ: "H5P interaktivní obsah"
3. Vlož embed kód do "H5P embed kód"
4. Ulož

#### Pro test:
1. Django Admin → Quizzes → Add Quiz
2. Vlož embed kód do "H5P embed kód"
3. Nastav časový limit, max pokusy, passing score
4. Ulož

### 4. Výsledky se ukládají automaticky

- Po dokončení H5P testu se výsledky automaticky uloží
- Zobrazí se skóre a zda test byl úspěšný
- Uloží se do QuizAttempt modelu

## Kde najdeš H5P

- **Materiály:** `/subjects/<subject>/<topic>/materials/<material_id>/`
- **Testy:** `/subjects/<subject>/<topic>/quizzes/<quiz_id>/attempt/`

## Technické detaily

- **JavaScript:** `static/js/h5p-integration.js`
- **API endpoint:** `/api/h5p/results/`
- **Dokumentace:** `docs/H5P_INTEGRATION.md`

## Tipy

1. **Responzivní design:** H5P iframe se automaticky přizpůsobí velikosti obrazovky
2. **Výsledky:** Automaticky se ukládají po dokončení testu
3. **Bezpečnost:** Používej pouze důvěryhodné H5P servery

