from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Vytvoří tabulku subjects_completedmaterial v databázi'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Zkontrolovat, zda tabulka už existuje
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='subjects_completedmaterial'
            """)
            if cursor.fetchone():
                self.stdout.write(
                    self.style.WARNING('Tabulka subjects_completedmaterial již existuje.')
                )
                return

            # Vytvořit tabulku
            cursor.execute("""
                CREATE TABLE subjects_completedmaterial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    material_id INTEGER NOT NULL,
                    completed_at DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
                    FOREIGN KEY (material_id) REFERENCES materials_material(id) ON DELETE CASCADE,
                    UNIQUE(user_id, material_id)
                )
            """)

            # Vytvořit indexy
            cursor.execute("""
                CREATE INDEX subjects_completedmaterial_user_id_material_id_idx 
                ON subjects_completedmaterial(user_id, material_id)
            """)

            self.stdout.write(
                self.style.SUCCESS('Tabulka subjects_completedmaterial byla úspěšně vytvořena.')
            )

