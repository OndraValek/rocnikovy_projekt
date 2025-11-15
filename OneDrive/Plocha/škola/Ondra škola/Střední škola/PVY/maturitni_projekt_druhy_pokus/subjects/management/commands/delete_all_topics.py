"""
Management příkaz pro smazání všech maturitních okruhů.
"""
from django.core.management.base import BaseCommand
from subjects.models import Topic, Subject
from materials.models import Material
from quizzes.models import Quiz
from forum.models import ForumThread


class Command(BaseCommand):
    help = 'Smaže všechny maturitní okruhy a související data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Potvrdit smazání (bez tohoto parametru se pouze zobrazí, co by bylo smazáno)',
        )

    def handle(self, *args, **options):
        confirm = options['confirm']
        
        # Spočítat, co bude smazáno
        topics_count = Topic.objects.count()
        subjects_count = Subject.objects.count()
        
        # Související data
        materials_count = Material.objects.count()
        quizzes_count = Quiz.objects.count()
        threads_count = ForumThread.objects.count()
        
        if not confirm:
            self.stdout.write(self.style.WARNING('=' * 70))
            self.stdout.write(self.style.WARNING('REŽIM NÁHLEDU - nic nebude smazáno'))
            self.stdout.write(self.style.WARNING('=' * 70))
            self.stdout.write('')
            self.stdout.write(f'Bylo by smazáno:')
            self.stdout.write(f'  - Okruhů (Topics): {topics_count}')
            self.stdout.write(f'  - Předmětů (Subjects): {subjects_count}')
            self.stdout.write(f'  - Materiálů: {materials_count}')
            self.stdout.write(f'  - Testů: {quizzes_count}')
            self.stdout.write(f'  - Vláken fóra: {threads_count}')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Pro skutečné smazání spusť:'))
            self.stdout.write(self.style.WARNING('  python manage.py delete_all_topics --confirm'))
            return
        
        # Skutečné smazání
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('MAZÁNÍ VŠECH MATURITNÍCH OKRUHŮ'))
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write('')
        
        # Smazat související data (kvůli CASCADE se smažou automaticky, ale pro jistotu)
        deleted_materials = Material.objects.all().delete()[0]
        deleted_quizzes = Quiz.objects.all().delete()[0]
        deleted_threads = ForumThread.objects.all().delete()[0]
        
        # Smazat okruhy
        deleted_topics = Topic.objects.all().delete()[0]
        
        # Smazat předměty
        deleted_subjects = Subject.objects.all().delete()[0]
        
        self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_topics} okruhů'))
        self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_subjects} předmětů'))
        self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_materials} materiálů'))
        self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_quizzes} testů'))
        self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_threads} vláken fóra'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Všechny maturitní okruhy byly úspěšně smazány!'))

