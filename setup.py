"""
Setup script pro automatickou inicializaci projektu po stažení z GitHubu.
"""
import os
import shutil
from pathlib import Path

def setup_project():
    """Automaticky nastaví projekt po stažení z GitHubu."""
    base_dir = Path(__file__).parent
    
    print("=" * 70)
    print("NASTAVENÍ PROJEKTU")
    print("=" * 70)
    print()
    
    # 1. Zkopírovat .env.example do .env, pokud .env neexistuje
    env_example = base_dir / '.env.example'
    env_file = base_dir / '.env'
    
    if env_example.exists():
        if not env_file.exists():
            print("📋 Kopírování .env.example do .env...")
            shutil.copy(env_example, env_file)
            print("✓ Soubor .env byl vytvořen z .env.example")
        else:
            print("✓ Soubor .env již existuje, přeskakuji kopírování")
    else:
        print("⚠️  Soubor .env.example nebyl nalezen")
    
    print()
    print("=" * 70)
    print("HOTOVO!")
    print("=" * 70)
    print()
    print("Další kroky:")
    print("1. Uprav .env soubor, pokud je potřeba")
    print("2. Spusť: python manage.py migrate")
    print("3. Spusť: python manage.py createsuperuser")
    print("4. Spusť: python manage.py create_social_apps")
    print("5. Spusť: python manage.py runserver")
    print()

if __name__ == '__main__':
    setup_project()

