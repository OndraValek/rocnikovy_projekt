"""
Skript pro smazání všech maturitních okruhů z databáze.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from subjects.models import Topic, Subject
from materials.models import Material
from quizzes.models import Quiz
from forum.models import ForumThread

print("=" * 70)
print("MAZÁNÍ VŠECH MATURITNÍCH OKRUHŮ")
print("=" * 70)
print()

# Spočítat, co bude smazáno
topics_count = Topic.objects.count()
subjects_count = Subject.objects.count()
materials_count = Material.objects.count()
quizzes_count = Quiz.objects.count()
threads_count = ForumThread.objects.count()

print(f'Bude smazáno:')
print(f'  - Okruhů (Topics): {topics_count}')
print(f'  - Předmětů (Subjects): {subjects_count}')
print(f'  - Materiálů: {materials_count}')
print(f'  - Testů: {quizzes_count}')
print(f'  - Vláken fóra: {threads_count}')
print()

if topics_count == 0 and subjects_count == 0:
    print("✓ Žádné okruhy ani předměty k smazání.")
else:
    # Smazat související data
    deleted_materials = Material.objects.all().delete()[0]
    deleted_quizzes = Quiz.objects.all().delete()[0]
    deleted_threads = ForumThread.objects.all().delete()[0]
    
    # Smazat okruhy
    deleted_topics = Topic.objects.all().delete()[0]
    
    # Smazat předměty
    deleted_subjects = Subject.objects.all().delete()[0]
    
    print("✓ Smazáno:")
    print(f'  - {deleted_topics} okruhů')
    print(f'  - {deleted_subjects} předmětů')
    print(f'  - {deleted_materials} materiálů')
    print(f'  - {deleted_quizzes} testů')
    print(f'  - {deleted_threads} vláken fóra')
    print()
    print("✓ Všechny maturitní okruhy byly úspěšně smazány!")

print()
print("=" * 70)

