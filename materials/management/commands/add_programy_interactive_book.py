from django.core.management.base import BaseCommand
from subjects.models import Topic
from materials.models import Material
from accounts.models import User


class Command(BaseCommand):
    help = 'Přidá materiál Programy a data - Interactive Book s H5P standalone'

    def add_arguments(self, parser):
        parser.add_argument(
            '--h5p-path',
            type=str,
            help='Cesta k H5P souboru (např. h5p/PD-interactive-book/) - pokud není zadáno, test se vytvoří bez h5p_path'
        )

    def handle(self, *args, **options):
        # Najít okruh
        topic = Topic.objects.filter(name__icontains='Programy a data').first()
        if not topic:
            self.stdout.write(self.style.ERROR('Okruh "Programy a data" nebyl nalezen.'))
            return
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        
        # Smazat všechny existující materiály s tímto názvem
        Material.objects.filter(topic=topic, title='Programy a data - Interactive Book').delete()
        
        h5p_path = options.get('h5p_path')
        
        # Vytvořit nový materiál s h5p_path (pokud je zadán)
        material = Material.objects.create(
            topic=topic,
            title='Programy a data - Interactive Book',
            description='Interaktivní kniha z oblasti programů a dat.',
            material_type='h5p',
            author=author,
            is_published=True,
            h5p_path=h5p_path,
            h5p_embed_code=None
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Vytvořen materiál: {material.title}'))
        if h5p_path:
            self.stdout.write(f'  h5p_path: {material.h5p_path}')
        else:
            self.stdout.write(self.style.WARNING('  h5p_path není nastaven. Použij add_h5p_quiz nebo extract_h5p pro nastavení.'))

