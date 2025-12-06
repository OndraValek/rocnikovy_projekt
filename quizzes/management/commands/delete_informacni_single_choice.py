from django.core.management.base import BaseCommand
from subjects.models import Topic
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Smaže test Informační systémy a databázové systémy - Single Choice Set'

    def handle(self, *args, **options):
        # Najít okruh
        topic = Topic.objects.filter(name__icontains='Informační systémy').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Informační systémy a databázové systémy" nebyl nalezen.'))
            return
        
        # Najít a smazat test
        quiz = Quiz.objects.filter(topic=topic, title='Informační systémy a databázové systémy - Single Choice Set').first()
        if quiz:
            quiz.delete()
            self.stdout.write(self.style.SUCCESS(f'✓ Smazán test: Informační systémy a databázové systémy - Single Choice Set'))
        else:
            self.stdout.write(self.style.WARNING('Test "Informační systémy a databázové systémy - Single Choice Set" nebyl nalezen.'))

