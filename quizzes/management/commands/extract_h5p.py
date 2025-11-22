"""
Management command pro rozbalení H5P souborů.

H5P soubory jsou vlastně ZIP archivy. Tento command:
1. Přijme .h5p soubor
2. Rozbalí ho do media/h5p/<slug>/
3. Volitelně aktualizuje Quiz model s h5p_path

Použití:
    python manage.py extract_h5p path/to/file.h5p --quiz-id 1
    python manage.py extract_h5p path/to/file.h5p --slug my-quiz
"""
import os
import zipfile
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Rozbalí H5P soubor (.h5p) do media složky'

    def add_arguments(self, parser):
        parser.add_argument(
            'h5p_file',
            type=str,
            help='Cesta k .h5p souboru'
        )
        parser.add_argument(
            '--quiz-id',
            type=int,
            help='ID Quiz objektu, který má být aktualizován s h5p_path'
        )
        parser.add_argument(
            '--slug',
            type=str,
            help='Slug pro pojmenování složky (pokud není --quiz-id)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Přepsat existující složku, pokud už existuje'
        )

    def handle(self, *args, **options):
        h5p_file = options['h5p_file']
        quiz_id = options.get('quiz_id')
        slug = options.get('slug')
        force = options.get('force', False)

        # Ověřit, že soubor existuje
        if not os.path.exists(h5p_file):
            raise CommandError(f'Soubor "{h5p_file}" neexistuje.')

        if not h5p_file.endswith('.h5p'):
            raise CommandError(f'Soubor "{h5p_file}" není .h5p soubor.')

        # Určit název složky
        if quiz_id:
            try:
                quiz = Quiz.objects.get(id=quiz_id)
                folder_name = f"quiz-{quiz.id}"
                self.stdout.write(f"Používám název složky z Quiz: {folder_name}")
            except Quiz.DoesNotExist:
                raise CommandError(f'Quiz s ID {quiz_id} neexistuje.')
        elif slug:
            folder_name = slug
        else:
            # Použít název souboru bez přípony
            folder_name = Path(h5p_file).stem

        # Cesta k rozbalenému H5P obsahu
        media_root = Path(settings.MEDIA_ROOT)
        h5p_folder = media_root / 'h5p' / folder_name

        # Zkontrolovat, zda složka už existuje
        if h5p_folder.exists() and not force:
            raise CommandError(
                f'Složka "{h5p_folder}" už existuje. Použijte --force pro přepsání.'
            )

        # Vytvořit složku
        h5p_folder.mkdir(parents=True, exist_ok=True)
        self.stdout.write(f"Vytváření složky: {h5p_folder}")

        # Rozbalit ZIP archiv
        try:
            with zipfile.ZipFile(h5p_file, 'r') as zip_ref:
                zip_ref.extractall(h5p_folder)
            self.stdout.write(self.style.SUCCESS(f"✓ H5P soubor rozbalen do: {h5p_folder}"))
        except zipfile.BadZipFile:
            raise CommandError(f'Soubor "{h5p_file}" není platný ZIP archiv.')
        except Exception as e:
            raise CommandError(f'Chyba při rozbalování: {e}')

        # Ověřit, že h5p.json existuje
        h5p_json = h5p_folder / 'h5p.json'
        if not h5p_json.exists():
            self.stdout.write(self.style.WARNING(
                "⚠ Varování: h5p.json nebyl nalezen. H5P obsah nemusí fungovat správně."
            ))

        # Relativní cesta pro uložení do databáze
        relative_path = f"h5p/{folder_name}/"

        # Aktualizovat Quiz, pokud je zadán quiz_id
        if quiz_id:
            quiz.h5p_path = relative_path
            quiz.save()
            self.stdout.write(self.style.SUCCESS(
                f"✓ Quiz (ID: {quiz_id}) aktualizován s h5p_path: {relative_path}"
            ))

        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("ROZBALENÍ DOKONČENO"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Relativní cesta: {relative_path}")
        self.stdout.write(f"Absolutní cesta: {h5p_folder}")
        self.stdout.write()
        self.stdout.write("Pro použití v Django Admin:")
        self.stdout.write(f"  h5p_path: {relative_path}")

