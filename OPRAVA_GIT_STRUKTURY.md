# Oprava Git struktury - soubory v rootu

Problém: Na GitHubu jsou soubory vnořené v `OneDrive/Plocha/škola/...` místo toho, aby byly v rootu repozitáře.

## Řešení

Spusť tyto příkazy v terminálu (PowerShell nebo CMD) v složce projektu:

```bash
# 1. Přejdi do složky projektu
cd "C:\Users\Ondra\OneDrive\Plocha\škola\Ondra škola\Střední škola\PVY\maturitni_projekt_druhy_pokus"

# 2. Odstraň starý .git (pokud existuje)
if exist .git rmdir /s /q .git

# 3. Vytvoř nový git repository
git init

# 4. Přidej remote
git remote add origin https://github.com/OndraValek/rocnikovy_projekt.git

# 5. Přidej všechny soubory
git add .

# 6. Vytvoř commit
git commit -m "Oprava struktury - soubory v rootu repozitare"

# 7. Pushni na GitHub (přepíše existující obsah)
git push -f origin main
```

**POZOR:** `git push -f` přepíše historii na GitHubu. Pokud máš důležité commity, nejdřív je zálohuj.

## Alternativní postup (bez force push)

Pokud nechceš použít force push:

```bash
# 1-6 stejné jako výše

# 7. Vytvoř novou branch
git checkout -b fix-structure

# 8. Pushni novou branch
git push origin fix-structure

# 9. Na GitHubu pak mergeuj fix-structure do main a smaž starou strukturu
```

