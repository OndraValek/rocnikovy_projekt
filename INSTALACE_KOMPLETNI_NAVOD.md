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

### 4. Nastavení databáze

**SQLite (jednodušší pro začátek):**
- Žádná další konfigurace není potřeba
- Databáze se vytvoří automaticky při migraci

**PostgreSQL (pro produkci):**
- Vytvoř soubor `.env` v kořenovém adresáři:
```
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=maturitni_projekt
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

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

### 7. Vytvoření inicializačních dat

**DŮLEŽITÉ:** Tento příkaz vytvoří předmět "Programové vybavení", 3 okruhy, materiál a 2 testy.

```bash
python manage.py create_initial_data
```

Tento příkaz vytvoří:
- ✅ Předmět "Programové vybavení"
- ✅ Okruh "Základy informatiky"
- ✅ Okruh "Programy a data"
- ✅ Okruh "Informační systémy a databázové systémy"
- ✅ H5P materiál "Základy informatiky"
- ✅ Test "Základy informatiky - Single Choice Set"
- ✅ Test "Základy informatiky - Question Set"

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

### 10. Spuštění vývojového serveru

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

# 3. Migrace databáze
python manage.py migrate

# 4. Vytvoření superuživatele
python manage.py createsuperuser

# 5. Vytvoření inicializačních dat (DŮLEŽITÉ!)
python manage.py create_initial_data

# 6. Spuštění serveru
python manage.py runserver
```

---

## ✅ Ověření, že vše funguje

Po spuštění serveru:

1. **Otevři:** http://localhost:8000
2. **Měl bys vidět:**
   - Předmět "Programové vybavení"
   - Po kliknutí: 3 okruhy
   - Po kliknutí na "Základy informatiky": materiál a 2 testy

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

