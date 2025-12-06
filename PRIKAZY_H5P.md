# Příkazy pro přidání H5P testů

## 1. Základy informatiky - Question Set

**Jeden příkaz, který vytvoří test a extrahuje H5P soubor:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Základy informatiky" --title "Základy informatiky - Question Set" --description "Soubor otázek z oblasti základů informatiky."
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `zaklady-informatiky-question-set...h5p`**

**Příklad (pokud je soubor na ploše):**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\zaklady-informatiky-question-set-xxx.h5p" --topic "Základy informatiky" --title "Základy informatiky - Question Set" --description "Soubor otázek z oblasti základů informatiky."
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Základy informatiky" --title "Základy informatiky - Question Set" --description "Soubor otázek z oblasti základů informatiky." --force
```

---

## 2. Základy informatiky - Interactive Book

**Možnost A: Vytvořit test a extrahovat H5P soubor najednou (doporučeno):**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Základy informatiky" --title "Základy informatiky - Interactive Book" --description "Interaktivní kniha z oblasti základů informatiky."
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `zaklady-informatiky-interactive-book...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\zaklady-informatiky-interactive-book-xxx.h5p" --topic "Základy informatiky" --title "Základy informatiky - Interactive Book" --description "Interaktivní kniha z oblasti základů informatiky."
```

**Možnost B: Pokud už máš extrahovaný H5P soubor, vytvoř jen test:**

```bash
python manage.py add_zaklady_interactive_book --h5p-path "h5p/quiz-13/"
```

(Nahraď `quiz-13` skutečným názvem složky s extrahovaným H5P souborem)

---

## 3. Programy a data - Single Choice Set

**Vytvořit test a extrahovat H5P soubor najednou:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Programy a data" --title "Programy a data - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti programů a dat." --type quiz
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `programy-a-data-single-choice-set...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\programy-a-data-single-choice-set-xxx.h5p" --topic "Programy a data" --title "Programy a data - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti programů a dat." --type quiz
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Programy a data" --title "Programy a data - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti programů a dat." --type quiz --force
```

---

## 4. Programy a data - Question Set

**Vytvořit test a extrahovat H5P soubor najednou:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Programy a data" --title "Programy a data - Question Set" --description "Soubor otázek z oblasti programů a dat." --type quiz
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `programy-a-data-question-set...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\programy-a-data-question-set-xxx.h5p" --topic "Programy a data" --title "Programy a data - Question Set" --description "Soubor otázek z oblasti programů a dat." --type quiz
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Programy a data" --title "Programy a data - Question Set" --description "Soubor otázek z oblasti programů a dat." --type quiz --force
```

---

## 5. Informační systémy a databázové systémy - Interactive Book

**Vytvořit materiál a extrahovat H5P soubor najednou:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Interactive Book" --description "Interaktivní kniha z oblasti informačních systémů a databázových systémů." --type material
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `informacni-systemy-a-databazove-systemy-interactive-book...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\informacni-systemy-a-databazove-systemy-interactive-book-xxx.h5p" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Interactive Book" --description "Interaktivní kniha z oblasti informačních systémů a databázových systémů." --type material
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Interactive Book" --description "Interaktivní kniha z oblasti informačních systémů a databázových systémů." --type material --force
```

---

## 6. Informační systémy a databázové systémy - Single Choice Set

**Vytvořit test a extrahovat H5P soubor najednou:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů." --type quiz
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `informacni-systemy-a-databazove-systemy-single-choice-set...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\informacni-systemy-a-databazove-systemy-single-choice-set-xxx.h5p" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů." --type quiz
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Single Choice Set" --description "Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů." --type quiz --force
```

---

## 7. Informační systémy a databázové systémy - Question Set

**Vytvořit test a extrahovat H5P soubor najednou:**

```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Question Set" --description "Soubor otázek z oblasti informačních systémů a databázových systémů." --type quiz
```

**Nahraď `<CESTA_K_SOUBORU>` skutečnou cestou k souboru `informacni-systemy-a-databazove-systemy-question-set...h5p`**

**Příklad:**
```bash
python manage.py add_h5p_quiz "C:\Users\Ondra\OneDrive\Plocha\informacni-systemy-a-databazove-systemy-question-set-xxx.h5p" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Question Set" --description "Soubor otázek z oblasti informačních systémů a databázových systémů." --type quiz
```

**Pokud chceš přepsat existující H5P složku:**
```bash
python manage.py add_h5p_quiz "<CESTA_K_SOUBORU>" --topic "Informační systémy a databázové systémy" --title "Informační systémy a databázové systémy - Question Set" --description "Soubor otázek z oblasti informačních systémů a databázových systémů." --type quiz --force
```

