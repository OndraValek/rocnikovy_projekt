# Kompletní návod k instalaci projektu

Tento návod obsahuje všechny příkazy potřebné k tomu, aby projekt fungoval po stažení z GitHubu.

## 📋 Krok za krokem

### 1. Stažení projektu z GitHubu

```bash
git clone https://github.com/OndraValek/rocnikovy_projekt.git
cd rocnikovy_projekt
```

### 2. Vytvoření virtuálního prostředí

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 4. Nastavení environment variables

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

Soubor `.env.example` obsahuje všechny potřebné proměnné včetně OAuth2 credentials, takže po zkopírování máš vše připravené. Pokud chceš použít jiné credentials, uprav je v `.env` souboru.

### 5. Spuštění migrací

```bash
python manage.py migrate
```

### 6. Vytvoření superuživatele

```bash
python manage.py createsuperuser
```

Zadej:
- Email (bude použit jako přihlašovací jméno)
- Heslo
- Potvrzení hesla

### 7. Vytvoření základní struktury (volitelné)

Pro vytvoření základní struktury (předmět "Programové vybavení" a 3 okruhy):

```bash
python manage.py setup_basic_data
```

**POZNÁMKA:** Tento příkaz vytvoří pouze předmět a okruhy. Materiály a testy musíš přidat ručně přes admin panel nebo pomocí jiných management commands.

### 8. Nastavení OAuth2 (volitelné, ale doporučeno)

Pro OAuth2 autentizaci přes Google, GitHub nebo Microsoft:

1. **Přidej OAuth2 credentials do `.env` souboru** (získej je z příslušných developer konzolí):
   ```env
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   MICROSOFT_CLIENT_ID=your-microsoft-client-id
   MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
   ```

2. **Spusť příkaz pro vytvoření Social Applications:**
   ```bash
   python manage.py create_social_apps
   ```
   
   Tento příkaz automaticky vytvoří Social Applications z hodnot v `.env` souboru. Pokud některé credentials chybí, příkaz přeskočí daného poskytovatele a zobrazí varování.

**DŮLEŽITÉ:** Redirect URIs v OAuth2 aplikacích musí být:
- Google: `http://localhost:8000/accounts/google/login/callback/`
- GitHub: `http://localhost:8000/accounts/github/login/callback/`
- Microsoft: `http://localhost:8000/accounts/microsoft/login/callback/`

Pro produkci změň `localhost:8000` na skutečnou doménu.

Podrobnější návod najdeš v `docs/OAUTH2_SETUP.md` nebo `OAUTH2_PODROBNY_NAVOD.md`.

### 8. Instalace h5p-standalone (volitelné, pro h5p-standalone integraci)

Pokud chceš používat h5p-standalone místo embed kódů:

1. **Stáhni h5p-standalone:**
   - Jdi na https://github.com/tunapanda/h5p-standalone/releases
   - Stáhni nejnovější release
   - Rozbal archiv

2. **Zkopíruj soubory do projektu:**
   ```
   static/h5p-player/
     ├── main.bundle.js      (z h5p-standalone/dist/)
     ├── frame.bundle.js     (z h5p-standalone/dist/)
     └── styles/
         └── h5p.css         (z h5p-standalone/dist/styles/)
   ```

3. **Spusť collectstatic:**
   ```bash
   python manage.py collectstatic
   ```

### 9. Vytvoření složky pro H5P obsah (volitelné)

Pokud chceš používat h5p-standalone s rozbalenými H5P soubory:

```bash
mkdir media\h5p
```

### 9. Spuštění vývojového serveru

```bash
python manage.py runserver
```

Aplikace bude dostupná na:
- **Frontend:** http://localhost:8000
- **Django Admin:** http://localhost:8000/django-admin/
- **Wagtail Admin:** http://localhost:8000/admin/

---

## 📝 Shrnutí všech příkazů (kopírovat najednou)

```bash
# 1. Aktivace virtuálního prostředí (pokud ještě není aktivní)
.\venv\Scripts\activate  # Windows
# nebo
source venv/bin/activate  # Linux/Mac

# 2. Instalace závislostí
pip install -r requirements.txt

# 3. Automatické nastavení .env (zkopíruje .env.example do .env)
setup.bat  # Windows
# nebo
./setup.sh  # Linux/Mac

# 4. Migrace databáze
python manage.py migrate

# 5. Vytvoření superuživatele
python manage.py createsuperuser

# 6. Nastavení OAuth2 (automaticky z .env)
python manage.py create_social_apps

# 7. Spuštění serveru
python manage.py runserver
```

---

## ✅ Ověření, že vše funguje

Po spuštění serveru:

1. **Otevři:** http://localhost:8000
2. **Měl bys vidět:**
   - Pokud jsi spustil `setup_basic_data`: Předmět "Programové vybavení" s 3 okruhy
   - Pokud ne: Prázdnou stránku (musíš přidat data ručně přes admin)

3. **Přihlas se do adminu:**
   - Django Admin: http://localhost:8000/django-admin/
   - Wagtail Admin: http://localhost:8000/admin/
   - Měl bys vidět všechny modely (Testy, Materiály, Předměty, atd.)

---

## 🔧 Volitelné příkazy (pokud potřebuješ)

### Přidání dalších okruhů s materiály a testy:

```bash
# Pro okruh "Programy a data"
python manage.py add_okruh_programy_a_data

# Pro okruh "Informační systémy a databázové systémy"
python manage.py add_okruh_informacni_systemy
```

### Rozbalení H5P souboru (pro h5p-standalone):

```bash
python manage.py extract_h5p cesta/k/souboru.h5p --quiz-id 1
```

### Vytvoření dalších uživatelů:

V Django Admin nebo Wagtail Admin:
- Jdi do "Uživatelé"
- Klikni na "Přidat uživatele"
- Vyplň údaje a nastav roli (Student, Učitel, Admin)

---

## 🐳 Použití s Docker (alternativa)

Pokud preferuješ Docker:

```bash
# Spuštění
docker-compose up --build

# Vytvoření superuživatele (v jiném terminálu)
docker-compose exec web python manage.py createsuperuser

# Vytvoření inicializačních dat
docker-compose exec web python manage.py create_initial_data
```

---

## ❓ Řešení problémů

### Chyba: "No module named 'X'"
```bash
pip install -r requirements.txt
```

### Chyba: "Unknown command: create_initial_data"
- Zkontroluj, že jsi v kořenovém adresáři projektu
- Zkontroluj, že soubor `management/commands/create_initial_data.py` existuje

### Chyba: "Table does not exist"
```bash
python manage.py migrate
```

### Databáze je prázdná
```bash
python manage.py create_initial_data
```

### H5P obsah se nenačítá
- Zkontroluj, že máš správně nastavené `h5p_embed_code` nebo `h5p_path`
- Pro h5p-standalone: zkontroluj, že jsou soubory v `static/h5p-player/`

---

## 📚 Další dokumentace

- `INSTALLATION.md` - Podrobný návod k instalaci
- `docs/H5P_STANDALONE_INTEGRATION.md` - Dokumentace h5p-standalone
- `H5P_POUZITI.md` - Jak používat H5P
- `README.md` - Obecné informace o projektu

---

## ✨ Hotovo!

Po dokončení všech kroků by měl projekt fungovat a měl bys vidět:
- ✅ Předmět "Programové vybavení"
- ✅ 3 okruhy
- ✅ Materiál a testy pro "Základy informatiky"
- ✅ Funkční admin rozhraní (Django i Wagtail)

