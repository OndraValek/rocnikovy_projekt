#!/usr/bin/env python
"""Skript pro vytvoření tabulky subjects_completedmaterial."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Zkontrolovat, zda tabulka už existuje
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='subjects_completedmaterial'
    """)
    if cursor.fetchone():
        print('Tabulka subjects_completedmaterial již existuje.')
    else:
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

        print('Tabulka subjects_completedmaterial byla úspěšně vytvořena.')

