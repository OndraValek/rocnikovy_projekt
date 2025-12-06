from django.core.management.base import BaseCommand
from subjects.models import Topic
from quizzes.models import Quiz
from accounts.models import User


class Command(BaseCommand):
    help = 'Přidá test Základy informatiky - Single Choice Set s H5P standalone'

    def handle(self, *args, **options):
        # Najít okruh
        topic = Topic.objects.filter(name__icontains='Základy informatiky').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Základy informatiky" nebyl nalezen.'))
            return
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        # Smazat všechny existující testy s tímto názvem
        Quiz.objects.filter(topic=topic, title='Základy informatiky - Single Choice Set').delete()
        Quiz.objects.filter(topic=topic, title='Základy informatiky - Question Set').delete()
        
        # Vytvořit nový test s h5p_path
        quiz = Quiz.objects.create(
            topic=topic,
            title='Základy informatiky - Single Choice Set',
            description='Test s jednoduchými výběrovými otázkami z oblasti základů informatiky.',
            author=author,
            is_published=True,
            passing_score=60,
            h5p_path='h5p/quiz-8/',
            h5p_embed_code=None
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz.title}'))
        self.stdout.write(f'  h5p_path: {quiz.h5p_path}')


