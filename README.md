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

### 3. Nastavení environment variables

**Automatické nastavení (doporučeno):**

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Nebo ručně:**

**Windows:**
```bash
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Soubor `.env.example` obsahuje všechny potřebné proměnné včetně OAuth2 credentials. Po zkopírování můžeš upravit `.env` soubor podle potřeby.

**DŮLEŽITÉ:** Soubor `.env.example` je commitován do Gitu a obsahuje OAuth2 credentials. Pokud chceš použít jiné credentials, uprav je v `.env` souboru.

### 4. Migrace databáze

```bash
python manage.py migrate
```

### 5. Vytvoření superuživatele

```bash
python manage.py createsuperuser
```

### 6. Vytvoření základní struktury (volitelné)

Pro vytvoření základní struktury (předmět "Programové vybavení" a 3 okruhy):

```bash
python manage.py setup_basic_data
```

**POZNÁMKA:** Tento příkaz vytvoří pouze předmět a okruhy. Materiály a testy musíš přidat ručně přes admin panel nebo pomocí jiných management commands.

### 7. Nastavení OAuth2 (volitelné)

Pokud chceš používat OAuth2 autentizaci (Google, GitHub, Microsoft):

1. **Přidej OAuth2 credentials do `.env` souboru** (získej je z příslušných developer konzolí):
   ```env
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   GITHUB_CLIENT_ID=your-client-id
   GITHUB_CLIENT_SECRET=your-client-secret
   MICROSOFT_CLIENT_ID=your-client-id
   MICROSOFT_CLIENT_SECRET=your-client-secret
   ```

2. **Spusť příkaz pro vytvoření Social Applications:**
   ```bash
   python manage.py create_social_apps
   ```
   
   Tento příkaz automaticky vytvoří Social Applications z hodnot v `.env` souboru. Pokud některé credentials chybí, příkaz přeskočí daného poskytovatele.

Podrobnější návod najdeš v `docs/OAUTH2_SETUP.md` nebo `OAUTH2_PODROBNY_NAVOD.md`.

### 8. Spuštění vývojového serveru

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

