from django.core.management.base import BaseCommand
from quizzes.models import Quiz
from materials.models import Material
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Zkontroluje cesty k H5P souborům v databázi a skutečné složky'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("KONTROLA H5P CEST")
        self.stdout.write("=" * 70)
        self.stdout.write()
        
        media_root = settings.MEDIA_ROOT
        h5p_dir = os.path.join(media_root, 'h5p')
        
        # Získat všechny skutečné složky
        actual_folders = []
        if os.path.exists(h5p_dir):
            for item in os.listdir(h5p_dir):
                item_path = os.path.join(h5p_dir, item)
                if os.path.isdir(item_path):
                    h5p_json = os.path.join(item_path, 'h5p.json')
                    exists = os.path.exists(h5p_json)
                    actual_folders.append((item, exists))
        
        self.stdout.write("SKUTEČNÉ SLOŽKY V media/h5p/:")
        for folder, has_json in actual_folders:
            status = "✓" if has_json else "✗ (chybí h5p.json)"
            self.stdout.write(f"  {status} {folder}")
        self.stdout.write()
        
        # Zkontrolovat testy
        self.stdout.write("TESTY V DATABÁZI:")
        quizzes = Quiz.objects.exclude(h5p_path__isnull=True).exclude(h5p_path='')
        for quiz in quizzes:
            h5p_path = quiz.h5p_path.rstrip('/')
            folder_name = h5p_path.replace('h5p/', '')
            folder_path = os.path.join(h5p_dir, folder_name)
            exists = os.path.exists(folder_path)
            has_json = os.path.exists(os.path.join(folder_path, 'h5p.json')) if exists else False
            
            status = "✓" if (exists and has_json) else "✗"
            self.stdout.write(f"  {status} {quiz.title}")
            self.stdout.write(f"      h5p_path: {quiz.h5p_path}")
            self.stdout.write(f"      Složka existuje: {exists}")
            if exists:
                self.stdout.write(f"      h5p.json existuje: {has_json}")
            self.stdout.write()
        
        # Zkontrolovat materiály
        self.stdout.write("MATERIÁLY V DATABÁZI:")
        materials = Material.objects.exclude(h5p_path__isnull=True).exclude(h5p_path='')
        for material in materials:
            h5p_path = material.h5p_path.rstrip('/')
            folder_name = h5p_path.replace('h5p/', '')
            folder_path = os.path.join(h5p_dir, folder_name)
            exists = os.path.exists(folder_path)
            has_json = os.path.exists(os.path.join(folder_path, 'h5p.json')) if exists else False
            
            status = "✓" if (exists and has_json) else "✗"
            self.stdout.write(f"  {status} {material.title}")
            self.stdout.write(f"      h5p_path: {material.h5p_path}")
            self.stdout.write(f"      Složka existuje: {exists}")
            if exists:
                self.stdout.write(f"      h5p.json existuje: {has_json}")
            self.stdout.write()
        
        self.stdout.write("=" * 70)

