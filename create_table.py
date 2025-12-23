import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subjects_completedmaterial'")
    if cursor.fetchone():
        print('Tabulka jiz existuje')
    else:
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
        cursor.execute("""
            CREATE INDEX subjects_completedmaterial_user_id_material_id_idx 
            ON subjects_completedmaterial(user_id, material_id)
        """)
        print('Tabulka vytvorena')

