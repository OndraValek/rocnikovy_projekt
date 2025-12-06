"""
Management command pro přidání H5P testu.

Vytvoří test v databázi a extrahuje H5P soubor.
"""
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from subjects.models import Topic
from quizzes.models import Quiz
from materials.models import Material
from accounts.models import User


class Command(BaseCommand):
    help = 'Vytvoří test a extrahuje H5P soubor'

    def add_arguments(self, parser):
        parser.add_argument('h5p_file', type=str, help='Cesta k .h5p souboru')
        parser.add_argument('--topic', type=str, required=True, help='Název okruhu (např. "Základy informatiky")')
        parser.add_argument('--title', type=str, required=True, help='Název testu nebo materiálu')
        parser.add_argument('--description', type=str, default='', help='Popis testu nebo materiálu')
        parser.add_argument('--type', type=str, choices=['quiz', 'material'], default='quiz', help='Typ: quiz nebo material (default: quiz)')
        parser.add_argument('--force', action='store_true', help='Přepsat existující složku')

    def handle(self, *args, **options):
        h5p_file = options['h5p_file']
        topic_name = options['topic']
        title = options['title']
        description = options['description']
        item_type = options['type']
        force = options['force']

        # Ověřit, že soubor existuje
        if not os.path.exists(h5p_file):
            raise CommandError(f'Soubor "{h5p_file}" neexistuje.')

        # Najít okruh
        topic = Topic.objects.filter(name__icontains=topic_name).first()
        if not topic:
            raise CommandError(f'Okruh "{topic_name}" nebyl nalezen.')

        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not author:
            raise CommandError('Nebyl nalezen žádný uživatel jako autor.')

        if item_type == 'quiz':
            # Vytvořit nebo získat test
            quiz, created = Quiz.objects.get_or_create(
                topic=topic,
                title=title,
                defaults={
                    'description': description,
                    'author': author,
                    'is_published': True,
                    'passing_score': 60,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz.title} (ID: {quiz.id})'))
            else:
                self.stdout.write(f'✓ Použit existující test: {quiz.title} (ID: {quiz.id})')

            # Extrahovat H5P soubor
            self.stdout.write(f'\nExtrahuji H5P soubor...')
            try:
                extract_args = ['extract_h5p', h5p_file, '--quiz-id', str(quiz.id)]
                if force:
                    extract_args.append('--force')
                call_command(*extract_args)
                self.stdout.write(self.style.SUCCESS(f'\n✓ Hotovo! Test je připraven s h5p_path: h5p/quiz-{quiz.id}/'))
            except Exception as e:
                raise CommandError(f'Chyba při extrakci H5P souboru: {e}')
        else:
            # Vytvořit nebo získat materiál
            material, created = Material.objects.get_or_create(
                topic=topic,
                title=title,
                defaults={
                    'description': description,
                    'material_type': 'h5p',
                    'author': author,
                    'is_published': True,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen materiál: {material.title} (ID: {material.id})'))
            else:
                self.stdout.write(f'✓ Použit existující materiál: {material.title} (ID: {material.id})')

            # Extrahovat H5P soubor
            self.stdout.write(f'\nExtrahuji H5P soubor...')
            try:
                # Pro materiál použijeme slug místo quiz-id
                slug = f"material-{material.id}"
                extract_args = ['extract_h5p', h5p_file, '--slug', slug]
                if force:
                    extract_args.append('--force')
                call_command(*extract_args)
                
                # Aktualizovat h5p_path
                material.h5p_path = f'h5p/{slug}/'
                material.save()
                
                self.stdout.write(self.style.SUCCESS(f'\n✓ Hotovo! Materiál je připraven s h5p_path: {material.h5p_path}'))
            except Exception as e:
                raise CommandError(f'Chyba při extrakci H5P souboru: {e}')

