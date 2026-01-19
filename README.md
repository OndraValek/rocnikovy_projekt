# Maturitní projekt - Programové vybavení

Webová aplikace pro přípravu studentů k maturitním zkouškám z předmětu Programové vybavení. Aplikace poskytuje komplexní systém pro organizaci studijních materiálů, interaktivních testů vytvořených v H5P a sledování pokroku studentů.

## 🎯 Hlavní funkce

- **📚 Studijní materiály** - Organizace materiálů podle předmětů a okruhů (PDF, video, H5P, odkazy)
- **📝 Interaktivní testy** - Testy vytvořené v H5P s automatickým ukládáním výsledků
- **📊 Statistiky** - Přehled výsledků testů s automatickým známkováním pro studenty i učitele
- **💬 Diskusní fórum** - Fórum pro každý okruh pro komunikaci mezi studenty a učiteli
- **👥 Role-based přístup** - Systém rolí (Student, Učitel, Administrátor) s odpovídajícími oprávněními
- **🔐 OAuth2 autentizace** - Přihlášení přes Google, GitHub nebo Microsoft
- **📱 Responzivní design** - Funguje na všech zařízeních od desktopů po mobily

## 🛠️ Technologie

- **Backend:** Django 4.2+ (Python)
- **CMS:** Wagtail 5.2+
- **Databáze:** PostgreSQL (produkce) / SQLite (vývoj)
- **Frontend:** Bootstrap 5, JavaScript (AJAX)
- **Interaktivní obsah:** H5P Standalone Player
- **Autentizace:** django-allauth (OAuth2)
- **API:** Django REST Framework
- **Deployment:** Docker, Docker Compose, Nginx, Gunicorn

## 📋 Požadavky

- Python 3.10+
- PostgreSQL (pro produkci) nebo SQLite (pro vývoj)
- Docker a Docker Compose (volitelné, pro Docker deployment)

## 🚀 Rychlý start

### Instalace pomocí Docker (doporučeno)

```bash
# Klonování repozitáře
git clone https://github.com/OndraValek/rocnikovy_projekt.git
cd rocnikovy_projekt

# Spuštění aplikace
docker compose up --build

# Aplikace bude dostupná na http://localhost:8000
# Výchozí superuživatel: admin@example.com / admin123
```

### Manuální instalace

#### 1. Vytvoření virtuálního prostředí

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2. Instalace závislostí

```bash
pip install -r requirements.txt
```

#### 3. Nastavení environment variables

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Nebo ručně zkopíruj `.env.example` do `.env` a uprav podle potřeby.

#### 4. Migrace databáze

```bash
python manage.py migrate
```

#### 5. Vytvoření superuživatele

```bash
python manage.py createsuperuser
```

#### 6. Vytvoření základní struktury (volitelné)

```bash
python manage.py setup_basic_data
```

#### 7. Nastavení OAuth2 (volitelné)

```bash
python manage.py create_social_apps
```

Podrobný návod najdeš v [`navody/OAUTH2_SETUP.md`](navody/OAUTH2_SETUP.md).

#### 8. Spuštění vývojového serveru

```bash
python manage.py runserver
```

Aplikace bude dostupná na `http://localhost:8000`

## 📁 Struktura projektu

```
maturitni_projekt_druhy_pokus/
├── accounts/          # Uživatelské účty a role
├── subjects/          # Předměty a maturitní okruhy
├── materials/         # Výukové materiály
├── quizzes/           # Testy a kvízy s H5P integrací
├── forum/             # Diskusní fórum
├── maturitni_projekt/ # Hlavní konfigurace projektu
├── templates/         # HTML šablony
├── static/            # Statické soubory (CSS, JS)
├── media/             # Uživatelsky nahrané soubory
├── navody/            # Dokumentace a návody
└── dokumentace/       # LaTeX dokumentace projektu
```

## 👥 Role uživatelů

### Student
- Prohlížení studijních materiálů
- Řešení testů
- Zobrazení vlastních statistik a výsledků
- Účast v diskusním fóru

### Učitel
- Všechny funkce studenta
- Vytváření a správa materiálů
- Vytváření a správa testů
- Zobrazení statistik všech studentů
- Moderování fóra

### Administrátor
- Plná kontrola nad systémem
- Správa uživatelů
- Přístup k Django Admin a Wagtail Admin

## 📚 Dokumentace

Všechny návody a dokumentace najdeš ve složce [`navody/`](navody/):

- [`INSTALACE_KOMPLETNI_NAVOD.md`](navody/INSTALACE_KOMPLETNI_NAVOD.md) - Kompletní návod k instalaci
- [`DOCKER.md`](navody/DOCKER.md) - Docker deployment
- [`H5P_STANDALONE_INTEGRATION.md`](navody/H5P_STANDALONE_INTEGRATION.md) - H5P integrace
- [`OAUTH2_SETUP.md`](navody/OAUTH2_SETUP.md) - Nastavení OAuth2
- [`WAGTAIL_ADMIN_INTEGRATION.md`](navody/WAGTAIL_ADMIN_INTEGRATION.md) - Wagtail CMS integrace

## 🐳 Docker

Pro produkční nasazení použij:

```bash
docker compose -f docker-compose.prod.yml up --build
```

Produkční konfigurace zahrnuje:
- Gunicorn jako WSGI server
- Nginx jako reverse proxy
- PostgreSQL databázi
- Automatické collectstatic

## 🔧 Management commands

```bash
# Vytvoření základní struktury
python manage.py setup_basic_data

# Vytvoření OAuth2 aplikací
python manage.py create_social_apps

# Rozbalení H5P souboru
python manage.py extract_h5p path/to/file.h5p --quiz-id 1
```

## 🌐 API Endpointy

Aplikace poskytuje REST API pro dynamické načítání obsahu:

- `/api/tasks/` - Všechny úlohy (materiály + testy)
- `/api/materials/` - Pouze materiály
- `/api/quizzes/` - Pouze testy
- `/quizzes/api/h5p/userdata/<content_id>/` - H5P uživatelská data
- `/quizzes/api/h5p/xapi/` - xAPI události z H5P

## 📝 Licence

Pro školní projekt.

## 👤 Autor

**Ondřej Valek**

- GitHub: [@OndraValek](https://github.com/OndraValek)
- Repozitář: [rocnikovy_projekt](https://github.com/OndraValek/rocnikovy_projekt)

## 🙏 Poděkování

- Django framework
- Wagtail CMS
- H5P Standalone Player
- Bootstrap 5
- Všem open-source projektům, které tento projekt využívá

---

**Video-prezentace:** https://www.youtube.com/watch?v=9XCEAN3dTI0&t=13s
