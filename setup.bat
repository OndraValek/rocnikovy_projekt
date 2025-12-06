@echo off
echo ======================================================================
echo NASTAVENI PROJEKTU
echo ======================================================================
echo.

REM Zkopírovat .env.example do .env, pokud .env neexistuje
if not exist .env (
    if exist .env.example (
        echo Kopírování .env.example do .env...
        copy .env.example .env
        echo ✓ Soubor .env byl vytvořen z .env.example
    ) else (
        echo ⚠️  Soubor .env.example nebyl nalezen
    )
) else (
    echo ✓ Soubor .env již existuje, přeskakuji kopírování
)

echo.
echo ======================================================================
echo HOTOVO!
echo ======================================================================
echo.
echo Další kroky:
echo 1. Uprav .env soubor, pokud je potřeba
echo 2. Spusť: python manage.py migrate
echo 3. Spusť: python manage.py createsuperuser
echo 4. Spusť: python manage.py create_social_apps
echo 5. Spusť: python manage.py runserver
echo.
pause

