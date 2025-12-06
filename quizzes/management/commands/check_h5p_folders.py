from django.core.management.base import BaseCommand
from quizzes.models import Quiz
from materials.models import Material
import json
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Zkontroluje obsah quiz-8 a quiz-6 složek'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("KONTROLA QUIZ-8 A QUIZ-6")
        self.stdout.write("=" * 70)
        self.stdout.write()
        
        media_root = settings.MEDIA_ROOT
        
        # Quiz-8
        quiz8_path = os.path.join(media_root, 'h5p', 'quiz-8', 'h5p.json')
        q8 = Quiz.objects.filter(h5p_path='h5p/quiz-8/').first()
        m8 = Material.objects.filter(h5p_path='h5p/quiz-8/').first()
        
        self.stdout.write("QUIZ-8:")
        if os.path.exists(quiz8_path):
            with open(quiz8_path, 'r', encoding='utf-8') as f:
                h5p_data = json.load(f)
                self.stdout.write(f"  Název v h5p.json: {h5p_data.get('title', 'N/A')}")
                self.stdout.write(f"  Typ: {h5p_data.get('mainLibrary', 'N/A')}")
        else:
            self.stdout.write("  h5p.json neexistuje!")
        self.stdout.write(f"  Test v databázi: {q8.title if q8 else 'NENALEZEN'}")
        self.stdout.write(f"  Materiál v databázi: {m8.title if m8 else 'NENALEZEN'}")
        self.stdout.write()
        
        # Quiz-6
        quiz6_path = os.path.join(media_root, 'h5p', 'quiz-6', 'h5p.json')
        q6 = Quiz.objects.filter(h5p_path='h5p/quiz-6/').first()
        m6 = Material.objects.filter(h5p_path='h5p/quiz-6/').first()
        
        self.stdout.write("QUIZ-6:")
        if os.path.exists(quiz6_path):
            with open(quiz6_path, 'r', encoding='utf-8') as f:
                h5p_data = json.load(f)
                self.stdout.write(f"  Název v h5p.json: {h5p_data.get('title', 'N/A')}")
                self.stdout.write(f"  Typ: {h5p_data.get('mainLibrary', 'N/A')}")
        else:
            self.stdout.write("  h5p.json neexistuje!")
        self.stdout.write(f"  Test v databázi: {q6.title if q6 else 'NENALEZEN'}")
        self.stdout.write(f"  Materiál v databázi: {m6.title if m6 else 'NENALEZEN'}")
        self.stdout.write()
        
        self.stdout.write("=" * 70)
        self.stdout.write("ZÁVĚR:")
        self.stdout.write("=" * 70)
        if q8 or m8:
            self.stdout.write(self.style.SUCCESS("✓ Quiz-8 je používán v databázi"))
        else:
            self.stdout.write(self.style.WARNING("✗ Quiz-8 NENÍ používán v databázi (můžeš ho smazat)"))
        
        if q6 or m6:
            self.stdout.write(self.style.SUCCESS("✓ Quiz-6 je používán v databázi"))
        else:
            self.stdout.write(self.style.WARNING("✗ Quiz-6 NENÍ používán v databázi (můžeš ho smazat)"))
        
        if (q8 or m8) and (q6 or m6):
            self.stdout.write()
            self.stdout.write(self.style.WARNING("⚠ POZOR: Oba quiz-8 i quiz-6 obsahují STEJNÝ obsah a oba jsou používané!"))
            self.stdout.write("   Měli byste jeden z nich smazat nebo přejmenovat.")

