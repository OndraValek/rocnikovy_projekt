# Maturitní projekt - Programové vybavení

Webová aplikace pro přípravu k maturitám s podporou studijních materiálů, testů a diskusního fóra.

## Technologie

- **Django 4.2+** - Webový framework
- **Wagtail 5.2+** - CMS pro správu obsahu
- **PostgreSQL** - Databáze (SQLite pro vývoj)
- **Tailwind CSS** - Stylování (plánováno)
- **H5P** - Interaktivní výukový obsah

## Struktura projektu

### Aplikace

- **accounts** - Uživatelské účty a role (Student, Učitel, Admin)
- **subjects** - Předměty a maturitní okruhy
- **materials** - Výukové materiály (PDF, video, H5P, odkazy)
- **quizzes** - Testy a kvízy s H5P integrací
- **forum** - Diskusní fórum pro každý okruh
- **maturitni_projekt/home** - Wagtail domovská stránka

## Instalace

### 1. Vytvoření virtuálního prostředí

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 3. Nastavení databáze

Pro vývoj můžete použít SQLite (výchozí) nebo PostgreSQL.

Pro PostgreSQL vytvořte soubor `.env`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=maturitni_projekt
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4. Migrace databáze

```bash
python manage.py migrate
```

### 5. Vytvoření superuživatele

```bash
python manage.py createsuperuser
```


### 7. Spuštění vývojového serveru

```bash
python manage.py runserver
```

Aplikace bude dostupná na `http://localhost:8000`

## Použití s Docker

Pro podrobné instrukce viz [DOCKER.md](DOCKER.md).

Rychlý start:

```bash
# Sestavení a spuštění
docker-compose up --build

# Aplikace bude dostupná na http://localhost:8000
# Výchozí superuživatel: admin@example.com / admin123
```

## Struktura dat

### Předmět (Subject)
- Název, slug, popis
- Obsahuje více okruhů

### Okruh (Topic)
- Název, slug, popis
- Patří k jednomu předmětu
- Má materiály, testy a diskusní fórum

### Materiál (Material)
- Typ: PDF, video, odkaz, H5P, text, obrázek
- Připojen k okruhu
- Může mít autora

### Test (Quiz)
- Připojen k okruhu
- Může obsahovat H5P embed kód
- Má časový limit a maximální počet pokusů
- Sleduje pokusy studentů (QuizAttempt)

### Diskusní fórum
- ForumThread - vlákno k okruhu
- ForumPost - příspěvky ve vláknech

## Role uživatelů

- **Student** - může číst materiály, řešit testy, psát do fóra
- **Učitel** - může přidávat materiály, vytvářet testy, moderovat fórum
- **Administrátor** - plná kontrola nad systémem

## H5P integrace

H5P obsah lze vložit pomocí iframe embed kódu do:
- Materiálů (typ H5P)
- Testů (h5p_embed_code)
- Wagtail stránek okruhů (H5P blok v StreamField)

## Příští kroky

- [ ] Vytvoření šablon (templates)
- [ ] Nastavení Tailwind CSS
- [ ] Vytvoření inicializačních dat pro předmět "Programové vybavení"
- [ ] Implementace API pro H5P výsledky
- [ ] Statistiky a přehledy pro učitele
- [ ] Export výsledků testů

## Licence

Pro školní projekt.

