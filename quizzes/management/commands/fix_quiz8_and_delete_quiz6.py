from django.core.management.base import BaseCommand
from subjects.models import Topic
from quizzes.models import Quiz
from accounts.models import User
import shutil
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Opraví připojení quiz-8 a smaže quiz-6'

    def handle(self, *args, **options):
        # Najít okruh "Informační systémy a databázové systémy"
        topic = Topic.objects.filter(name__icontains='Informační systémy').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Informační systémy a databázové systémy" nebyl nalezen.'))
            return
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        # Najít nebo vytvořit test "Informační systémy a databázové systémy - Single Choice Set"
        quiz, created = Quiz.objects.get_or_create(
            topic=topic,
            title='Informační systémy a databázové systémy - Single Choice Set',
            defaults={
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/quiz-8/',
                'h5p_embed_code': None
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen test: {quiz.title}'))
        else:
            # Aktualizovat h5p_path pokud už existuje
            quiz.h5p_path = 'h5p/quiz-8/'
            quiz.h5p_embed_code = None
            quiz.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Aktualizován test: {quiz.title}'))
        
        self.stdout.write(f'  h5p_path: {quiz.h5p_path}')
        self.stdout.write()
        
        # Najít a opravit test "Základy informatiky - Single Choice Set" (měl by používat quiz-8, ale obsahuje špatný obsah)
        zaklady_topic = Topic.objects.filter(name__icontains='Základy informatiky').first()
        if zaklady_topic:
            zaklady_quiz = Quiz.objects.filter(topic=zaklady_topic, title='Základy informatiky - Single Choice Set', h5p_path='h5p/quiz-8/').first()
            if zaklady_quiz:
                # Tento test má špatný h5p_path, měl by používat jiný (nebo nemá být)
                self.stdout.write(self.style.WARNING(f'⚠ Test "{zaklady_quiz.title}" používá quiz-8, ale obsahuje špatný obsah.'))
                self.stdout.write('   Měl by používat jiný H5P soubor pro "Základy informatiky".')
                # Necháme ho být, protože uživatel možná má jiný soubor
        
        # Smazat quiz-6 složku
        media_root = settings.MEDIA_ROOT
        quiz6_path = os.path.join(media_root, 'h5p', 'quiz-6')
        
        if os.path.exists(quiz6_path):
            try:
                shutil.rmtree(quiz6_path)
                self.stdout.write(self.style.SUCCESS(f'✓ Složka quiz-6 smazána: {quiz6_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Chyba při mazání quiz-6: {e}'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Složka quiz-6 neexistuje.'))
        
        self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Hotovo!'))

