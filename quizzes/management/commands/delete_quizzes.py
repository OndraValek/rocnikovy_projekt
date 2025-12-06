"""
Management command pro smazání konkrétních testů.
"""
from django.core.management.base import BaseCommand, CommandError
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Smaže testy podle názvu (Question Set a Single Choice Set)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Potvrdit smazání (bez tohoto parametru se jen zobrazí náhled)'
        )

    def handle(self, *args, **options):
        confirm = options.get('confirm', False)
        
        # Najít testy podle názvu
        quiz1 = Quiz.objects.filter(title__icontains='Question Set').first()
        quiz2 = Quiz.objects.filter(title__icontains='Single Choice Set').first()
        
        quizzes_to_delete = []
        if quiz1:
            quizzes_to_delete.append(quiz1)
        if quiz2:
            quizzes_to_delete.append(quiz2)
        
        if not quizzes_to_delete:
            self.stdout.write(self.style.WARNING('Žádné testy k smazání nebyly nalezeny.'))
            self.stdout.write('\nVšechny dostupné testy:')
            for q in Quiz.objects.all():
                self.stdout.write(f'  - ID: {q.id}, Název: {q.title}')
            return
        
        # Zobrazit, co bude smazáno
        self.stdout.write('=' * 70)
        self.stdout.write('TESTY K SMAZÁNÍ:')
        self.stdout.write('=' * 70)
        for quiz in quizzes_to_delete:
            self.stdout.write(f'  - ID: {quiz.id}, Název: {quiz.title}')
        
        if not confirm:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('REŽIM NÁHLEDU - nic nebude smazáno'))
            self.stdout.write(self.style.WARNING('Pro skutečné smazání spusť:'))
            self.stdout.write(self.style.WARNING('  python manage.py delete_quizzes --confirm'))
            return
        
        # Skutečné smazání
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('MAZÁNÍ TESTŮ...'))
        
        deleted_count = 0
        for quiz in quizzes_to_delete:
            title = quiz.title
            quiz.delete()
            self.stdout.write(self.style.SUCCESS(f'✓ Smazán test: {title}'))
            deleted_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Úspěšně smazáno {deleted_count} testů.'))

