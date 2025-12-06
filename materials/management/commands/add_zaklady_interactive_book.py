from django.core.management.base import BaseCommand
from subjects.models import Topic
from materials.models import Material
from quizzes.models import Quiz
from accounts.models import User


class Command(BaseCommand):
    help = 'Přidá materiál Základy informatiky - Interactive Book a smaže test'

    def handle(self, *args, **options):
        # Najít okruh
        topic = Topic.objects.filter(name__icontains='Základy informatiky').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Základy informatiky" nebyl nalezen.'))
            return
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        # Smazat test Interactive Book z quizzes
        deleted_count = Quiz.objects.filter(topic=topic, title='Základy informatiky - Interactive Book').delete()[0]
        if deleted_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✓ Smazáno {deleted_count} test(ů) Interactive Book z quizzes'))
        
        # Smazat všechny existující materiály s tímto názvem
        Material.objects.filter(topic=topic, title='Základy informatiky - Interactive Book').delete()
        
        # Vytvořit nový materiál s h5p_path
        material = Material.objects.create(
            topic=topic,
            title='Základy informatiky - Interactive Book',
            description='Interaktivní kniha z oblasti základů informatiky.',
            material_type='h5p',
            author=author,
            is_published=True,
            h5p_path='h5p/quiz-14/',
            h5p_embed_code=None
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen materiál: {material.title}'))
        self.stdout.write(f'  h5p_path: {material.h5p_path}')

