"""
Management command pro vytvoření testů pro okruh.
"""
from django.core.management.base import BaseCommand, CommandError
from quizzes.models import Quiz
from subjects.models import Topic
from accounts.models import User


class Command(BaseCommand):
    help = 'Vytvoří testy (Question Set a Single Choice Set) pro zadaný okruh'

    def add_arguments(self, parser):
        parser.add_argument(
            'topic_id',
            type=int,
            help='ID okruhu, pro který se vytvoří testy'
        )
        parser.add_argument(
            '--author-id',
            type=int,
            help='ID autora testů (pokud není zadáno, použije se první superuser)'
        )

    def handle(self, *args, **options):
        topic_id = options['topic_id']
        author_id = options.get('author_id')
        
        # Najít okruh
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise CommandError(f'Okruh s ID {topic_id} neexistuje.')
        
        # Najít autora
        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                raise CommandError(f'Uživatel s ID {author_id} neexistuje.')
        else:
            # Použít prvního superusera nebo prvního uživatele
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                author = User.objects.first()
            if not author:
                raise CommandError('Nebyl nalezen žádný uživatel. Vytvořte nejdřív uživatele.')
        
        self.stdout.write(f'Vytváření testů pro okruh: {topic.name}')
        self.stdout.write(f'Autor: {author.email}')
        self.stdout.write('')
        
        # Vytvořit Question Set test
        quiz1, created1 = Quiz.objects.get_or_create(
            topic=topic,
            title=f'{topic.name} - Question Set',
            defaults={
                'description': f'Soubor otázek z oblasti {topic.name.lower()}.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
            }
        )
        
        if created1:
            self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz1.title} (ID: {quiz1.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Test už existuje: {quiz1.title} (ID: {quiz1.id})'))
        
        # Vytvořit Single Choice Set test
        quiz2, created2 = Quiz.objects.get_or_create(
            topic=topic,
            title=f'{topic.name} - Single Choice Set',
            defaults={
                'description': f'Test s jednoduchými výběrovými otázkami z oblasti {topic.name.lower()}.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
            }
        )
        
        if created2:
            self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz2.title} (ID: {quiz2.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Test už existuje: {quiz2.title} (ID: {quiz2.id})'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Hotovo!'))

