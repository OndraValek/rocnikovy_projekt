from django.core.management.base import BaseCommand
from subjects.models import Topic
from quizzes.models import Quiz
from accounts.models import User


class Command(BaseCommand):
    help = 'Přidá test Základy informatiky - Interactive Book s H5P standalone'

    def add_arguments(self, parser):
        parser.add_argument(
            '--h5p-path',
            type=str,
            help='Cesta k H5P souboru (např. h5p/quiz-13/) - pokud není zadáno, test se vytvoří bez h5p_path'
        )

    def handle(self, *args, **options):
        # Najít okruh
        topic = Topic.objects.filter(name__icontains='Základy informatiky').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Základy informatiky" nebyl nalezen.'))
            return
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        # Smazat všechny existující testy s tímto názvem
        Quiz.objects.filter(topic=topic, title='Základy informatiky - Interactive Book').delete()
        
        h5p_path = options.get('h5p_path')
        
        # Vytvořit nový test s h5p_path (pokud je zadán)
        quiz = Quiz.objects.create(
            topic=topic,
            title='Základy informatiky - Interactive Book',
            description='Interaktivní kniha z oblasti základů informatiky.',
            author=author,
            is_published=True,
            passing_score=60,
            h5p_path=h5p_path,
            h5p_embed_code=None
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz.title}'))
        if h5p_path:
            self.stdout.write(f'  h5p_path: {quiz.h5p_path}')
        else:
            self.stdout.write(self.style.WARNING('  h5p_path není nastaven. Použij add_h5p_quiz nebo extract_h5p pro nastavení.'))

