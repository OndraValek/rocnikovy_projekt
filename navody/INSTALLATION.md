# Návod k instalaci a spuštění

## Rychlý start

### 1. Instalace závislostí

```bash
# Vytvoření virtuálního prostředí
python -m venv venv

# Aktivace (Windows)
.\venv\Scripts\activate

# Aktivace (Linux/Mac)
source venv/bin/activate

# Instalace balíčků
pip install -r requirements.txt
```

### 2. Nastavení databáze

Pro vývoj můžete použít SQLite (výchozí) nebo PostgreSQL.

**SQLite (jednodušší pro začátek):**
- Žádná další konfigurace není potřeba
- Databáze se vytvoří automaticky při migraci

**PostgreSQL:**
- Vytvořte soubor `.env` v kořenovém adresáři:
```
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=maturitni_projekt
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 3. Migrace databáze

```bash
python manage.py migrate
```

### 4. Vytvoření superuživatele

```bash
python manage.py createsuperuser
```

Zadejte email, heslo a další údaje. Email bude použit jako přihlašovací jméno.

### 5. Vytvoření inicializačních dat

```bash
python manage.py create_initial_data
```

Tento příkaz vytvoří:
- Předmět "Programové vybavení"
- 6 základních maturitních okruhů

### 6. Spuštění serveru

```bash
python manage.py runserver
```

Aplikace bude dostupná na:
- Frontend: http://localhost:8000
- Admin panel: http://localhost:8000/admin
- Wagtail admin: http://localhost:8000/admin

## Použití s Docker

```bash
# Spuštění
docker-compose up --build

# Vytvoření superuživatele (v jiném terminálu)
docker-compose exec web python manage.py createsuperuser

# Vytvoření inicializačních dat
docker-compose exec web python manage.py create_initial_data
```

## První kroky po instalaci

1. **Přihlaste se do admin panelu** (http://localhost:8000/admin)
2. **Vytvořte uživatele s rolí Učitel:**
   - Jděte na "Uživatelé" → "Přidat uživatele"
   - Vyplňte email, heslo a nastavte roli na "Učitel"
3. **Přidejte materiály a testy:**
   - V admin panelu můžete přidávat materiály, testy a spravovat obsah
4. **Upravte okruhy:**
   - V admin panelu můžete upravit názvy a popisy okruhů podle skutečných maturitních okruhů

## Struktura rolí

- **Student** - může číst materiály, řešit testy, psát do fóra
- **Učitel** - může přidávat materiály, vytvářet testy, moderovat fórum
- **Administrátor** - plná kontrola nad systémem

## Přidávání H5P obsahu

1. Vytvořte H5P obsah na H5P.org nebo v jiném H5P editoru
2. Zkopírujte iframe embed kód
3. V admin panelu při vytváření materiálu nebo testu:
   - Vyberte typ "H5P interaktivní obsah"
   - Vložte embed kód do pole "H5P embed kód"

## Řešení problémů

### Chyba při migraci
- Zkontrolujte, zda máte nainstalované všechny závislosti
- Zkontrolujte připojení k databázi (pokud používáte PostgreSQL)

### Chyba při přihlášení
- Ujistěte se, že jste vytvořili superuživatele
- Zkontrolujte, že používáte email jako přihlašovací jméno

### Statické soubory se nezobrazují
```bash
python manage.py collectstatic --noinput
```

