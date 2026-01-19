# Dokumentace projektu

## Diagramy

### Datový model (PlantUML)

Soubor `database_model.puml` obsahuje ER diagram datového modelu aplikace.

**Jak zobrazit:**
1. Nainstalujte PlantUML plugin do VS Code nebo použijte online editor: http://www.plantuml.com/plantuml/uml/
2. Otevřete soubor `docs/database_model.puml`
3. Diagram zobrazí strukturu databáze s vztahy mezi tabulkami

**Struktura modelu:**
- **User** - Uživatelé systému (studenti, učitelé, administrátoři)
- **UserProfile** - Rozšířený profil uživatele
- **Subject** - Maturitní předměty
- **Topic** - Okruhy v rámci předmětů
- **Material** - Výukové materiály (PDF, video, H5P, odkazy)
- **Quiz** - Testy a kvízy s H5P integrací
- **QuizAttempt** - Pokusy studentů o vyplnění testů
- **ForumThread** - Diskusní vlákna
- **ForumPost** - Příspěvky ve fóru

### USE CASE diagram (PlantUML)

Soubor `use_case_diagram.puml` obsahuje diagram případů použití aplikace.

**Jak zobrazit:**
1. Nainstalujte PlantUML plugin do VS Code nebo použijte online editor
2. Otevřete soubor `docs/use_case_diagram.puml`
3. Diagram zobrazí všechny funkcionality aplikace podle rolí uživatelů

**Aktéři:**
- **Student** - Může prohlížet obsah, řešit testy, účastnit se diskusí
- **Teacher** - Může vše co student + vytvářet a spravovat obsah
- **Admin** - Má plná oprávnění včetně správy uživatelů

## Export diagramů

Pro export do PNG nebo SVG můžete použít:

```bash
# S PlantUML JAR
java -jar plantuml.jar docs/database_model.puml
java -jar plantuml.jar docs/use_case_diagram.puml

# Nebo použijte online editor na http://www.plantuml.com/plantuml/uml/
```

## Alternativní nástroje

- **dbdiagram.io** - Pro ER diagramy (https://dbdiagram.io/)
- **Draw.io** - Univerzální nástroj pro diagramy
- **Lucidchart** - Profesionální nástroj pro diagramy

