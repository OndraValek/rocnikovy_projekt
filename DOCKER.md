# Dockerizace aplikace

Tento projekt je připraven pro spuštění pomocí Docker a Docker Compose.

## Požadavky

- [Docker](https://www.docker.com/get-started) (verze 20.10 nebo novější)
- [Docker Compose](https://docs.docker.com/compose/install/) (verze 1.29 nebo novější)

## Rychlý start

### 1. Klonování a příprava

```bash
# Pokud ještě nemáš projekt, naklonuj ho
git clone <repository-url>
cd maturitni_projekt_druhy_pokus
```

### 2. Spuštění aplikace

```bash
# Sestavení a spuštění kontejnerů
docker-compose up --build
```

Aplikace bude dostupná na: http://localhost:8000

### 3. Vytvoření superuživatele (volitelné)

Pokud chceš vytvořit vlastního superuživatele:

```bash
docker-compose exec web python manage.py createsuperuser
```

Výchozí superuživatel:
- Email: `admin@example.com`
- Heslo: `admin123`

## Příkazy

### Spuštění v pozadí

```bash
docker-compose up -d
```

### Zastavení

```bash
docker-compose down
```

### Zastavení a smazání databáze

```bash
docker-compose down -v
```

### Zobrazení logů

```bash
docker-compose logs -f web
```

### Spuštění Django příkazů

```bash
# Migrace
docker-compose exec web python manage.py migrate

# Collectstatic
docker-compose exec web python manage.py collectstatic

# Django shell
docker-compose exec web python manage.py shell

# Vytvoření superuživatele
docker-compose exec web python manage.py createsuperuser
```

### Přístup do kontejneru

```bash
docker-compose exec web bash
```

## Struktura

- `Dockerfile` - Definice Docker image pro Django aplikaci
- `docker-compose.yml` - Orchestrace služeb (web + databáze)
- `docker-entrypoint.sh` - Skript pro inicializaci (migrace, collectstatic, superuser)
- `.dockerignore` - Soubory, které se nezahrnou do image

## Služby

### Web (Django aplikace)
- Port: `8000`
- Image: Sestaveno z `Dockerfile`
- Volumes: 
  - Projektový kód (pro vývoj)
  - Static files
  - Media files

### Databáze (PostgreSQL)
- Port: `5432`
- Image: `postgres:15`
- Databáze: `maturitni_projekt`
- Uživatel: `postgres`
- Heslo: `postgres`

## Environment Variables

Můžeš upravit proměnné prostředí v `docker-compose.yml`:

```yaml
environment:
  - DB_HOST=db
  - DB_NAME=maturitni_projekt
  - DB_USER=postgres
  - DB_PASSWORD=postgres
  - SECRET_KEY=dev-secret-key-change-in-production
  - DEBUG=1
  - ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## Produkce

⚠️ **Důležité:** Tato konfigurace je pro vývoj! Pro produkci:

1. Změň `DEBUG=0`
2. Nastav silný `SECRET_KEY`
3. Použij produkční settings (`maturitni_projekt.settings.production`)
4. Nastav správné `ALLOWED_HOSTS`
5. Použij reverse proxy (nginx) pro statické soubory
6. Použij WSGI server (gunicorn) místo `runserver`

## Řešení problémů

### Port je již používán

```bash
# Změň port v docker-compose.yml
ports:
  - "8001:8000"  # Místo 8000:8000
```

### Databáze se nepřipojuje

```bash
# Zkontroluj, že databáze běží
docker-compose ps

# Zkontroluj logy
docker-compose logs db
```

### Migrace selhávají

```bash
# Spusť migrace ručně
docker-compose exec web python manage.py migrate
```

### Statické soubory se nezobrazují

```bash
# Spusť collectstatic
docker-compose exec web python manage.py collectstatic --noinput
```

## Aktualizace

Po změnách v kódu:

```bash
# Restartuj kontejnery
docker-compose restart web
```

Po změnách v `requirements.txt`:

```bash
# Znovu sestav image
docker-compose up --build
```

## Odstranění

```bash
# Zastav a odstraň kontejnery
docker-compose down

# Zastav, odstraň kontejnery a volumes (včetně databáze)
docker-compose down -v

# Odstranění image
docker rmi maturitni_projekt_druhy_pokus_web
```

