# Docker Setup Guide

Tento projekt obsahuje kompletní Docker konfiguraci pro vývoj i produkci.

## Požadavky

- Docker (verze 20.10 nebo novější)
- Docker Compose (verze 1.29 nebo novější)

## Rychlý start (vývoj)

1. **Naklonujte repozitář** (pokud ještě nemáte):
   ```bash
   git clone <repository-url>
   cd maturitni_projekt_druhy_pokus
   ```

2. **Spusťte aplikaci pomocí Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Aplikace bude dostupná na**:
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin/
   - Wagtail Admin: http://localhost:8000/wagtail-admin/
   - Databáze: localhost:5432

4. **Výchozí superuser**:
   - Email: `admin@example.com`
   - Heslo: `admin123`

## Vývojové prostředí

### Spuštění

```bash
docker-compose up
```

### Spuštění na pozadí

```bash
docker-compose up -d
```

### Zobrazení logů

```bash
docker-compose logs -f web
```

### Zastavení

```bash
docker-compose down
```

### Zastavení a smazání dat

```bash
docker-compose down -v
```

### Přístup do kontejneru

```bash
docker-compose exec web bash
```

### Spuštění Django příkazů

```bash
# Migrace
docker-compose exec web python manage.py migrate

# Vytvoření superuseru
docker-compose exec web python manage.py createsuperuser

# Shell
docker-compose exec web python manage.py shell

# Collectstatic
docker-compose exec web python manage.py collectstatic
```

## Produkční prostředí

### Příprava

1. **Vytvořte `.env` soubor** (můžete použít `.env.example` jako šablonu):
   ```bash
   cp .env.example .env
   ```

2. **Upravte `.env` soubor** s produkčními hodnotami:
   - `SECRET_KEY` - vygenerujte bezpečný klíč
   - `DB_PASSWORD` - silné heslo pro databázi
   - `ALLOWED_HOSTS` - seznam povolených domén
   - `DEBUG=0` - vypněte debug mód
   - `DJANGO_SETTINGS_MODULE=maturitni_projekt.settings.production`

3. **Spusťte produkční prostředí**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

### Produkční příkazy

```bash
# Spuštění
docker-compose -f docker-compose.prod.yml up -d

# Zobrazení logů
docker-compose -f docker-compose.prod.yml logs -f

# Zastavení
docker-compose -f docker-compose.prod.yml down

# Restart
docker-compose -f docker-compose.prod.yml restart
```

## Struktura Docker konfigurace

- **Dockerfile** - Definice Docker image pro Django aplikaci
- **docker-compose.yml** - Vývojové prostředí s hot reload
- **docker-compose.prod.yml** - Produkční prostředí s Nginx a Gunicorn
- **docker-entrypoint.sh** - Entrypoint script pro inicializaci
- **nginx.conf** - Nginx konfigurace pro produkci
- **.dockerignore** - Soubory ignorované při build

## Databáze

### Přístup k databázi

```bash
docker-compose exec db psql -U postgres -d maturitni_projekt
```

### Záloha databáze

```bash
docker-compose exec db pg_dump -U postgres maturitni_projekt > backup.sql
```

### Obnovení databáze

```bash
docker-compose exec -T db psql -U postgres maturitni_projekt < backup.sql
```

## Volumes

Projekt používá následující Docker volumes:

- `postgres_data` - Databázová data
- `static_volume` - Statické soubory (CSS, JS, obrázky)
- `media_volume` - Uživatelsky nahrané soubory (H5P, dokumenty, videa)

## Řešení problémů

### Port je již používán

Pokud port 8000 nebo 5432 je již používán, změňte porty v `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Změňte 8001 na jiný port
```

### Databáze se nespustí

Zkontrolujte logy:
```bash
docker-compose logs db
```

### Statické soubory se nezobrazují

Spusťte collectstatic:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Změny v kódu se neprojevují

Vývojové prostředí má volume mount, takže změny by se měly projevit automaticky. Pokud ne, restartujte kontejner:
```bash
docker-compose restart web
```

## Bezpečnost

⚠️ **DŮLEŽITÉ PRO PRODUKCI:**

1. Změňte výchozí `SECRET_KEY` v `.env`
2. Použijte silné heslo pro databázi
3. Nastavte `DEBUG=0` v produkci
4. Nakonfigurujte `ALLOWED_HOSTS` správně
5. Použijte HTTPS v produkci (konfigurace SSL v Nginx)
6. Změňte výchozí superuser heslo

## Další informace

Pro více informací o projektu viz hlavní `README.md`.

