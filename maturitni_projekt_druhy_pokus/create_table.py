import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Zkontrolovat, zda tabulka existuje
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='subjects_completedtopic'
    """)
    exists = cursor.fetchone()
    
    if not exists:
        # Vytvořit tabulku
        cursor.execute("""
            CREATE TABLE subjects_completedtopic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                completed_at DATETIME NOT NULL,
                topic_id INTEGER NOT NULL REFERENCES subjects_topic(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
                UNIQUE(user_id, topic_id)
            )
        """)
        
        # Vytvořit index
        cursor.execute("""
            CREATE INDEX subjects_co_user_id_idx ON subjects_completedtopic(user_id, topic_id)
        """)
        
        print("Tabulka subjects_completedtopic byla úspěšně vytvořena!")
    else:
        print("Tabulka subjects_completedtopic již existuje.")

