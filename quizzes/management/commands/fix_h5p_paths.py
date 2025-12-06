from django.core.management.base import BaseCommand
from quizzes.models import Quiz
from materials.models import Material
from subjects.models import Topic


class Command(BaseCommand):
    help = 'Opraví cesty k H5P souborům po přejmenování složek'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("OPRAVA H5P CEST PO PŘEJMENOVÁNÍ SLOŽEK")
        self.stdout.write("=" * 70)
        self.stdout.write()
        
        # Najít okruhy
        zaklady_topic = Topic.objects.filter(name__icontains='Základy informatiky').first()
        informacni_topic = Topic.objects.filter(name__icontains='Informační systémy').first()
        
        # Opravit testy pro "Základy informatiky"
        if zaklady_topic:
            # Single Choice Set
            quiz1 = Quiz.objects.filter(topic=zaklady_topic, title__icontains='Single Choice Set').first()
            if quiz1:
                old_path = quiz1.h5p_path
                quiz1.h5p_path = 'h5p/ZI-single-choice/'
                quiz1.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opraven test: {quiz1.title}'))
                self.stdout.write(f'  {old_path} → {quiz1.h5p_path}')
            
            # Question Set
            quiz2 = Quiz.objects.filter(topic=zaklady_topic, title__icontains='Question Set').first()
            if quiz2:
                old_path = quiz2.h5p_path
                quiz2.h5p_path = 'h5p/ZI-question-set/'
                quiz2.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opraven test: {quiz2.title}'))
                self.stdout.write(f'  {old_path} → {quiz2.h5p_path}')
            
            # Interactive Book (materiál)
            material = Material.objects.filter(topic=zaklady_topic, title__icontains='Interactive Book').first()
            if material:
                old_path = material.h5p_path
                material.h5p_path = 'h5p/ZI-interactive-book/'
                material.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opraven materiál: {material.title}'))
                self.stdout.write(f'  {old_path} → {material.h5p_path}')
        
        # Opravit test pro "Informační systémy a databázové systémy"
        # Tento test by měl používat jiný H5P soubor, ale zatím použijeme ZI-single-choice
        # (protože obsahuje stejný obsah podle h5p.json)
        if informacni_topic:
            quiz3 = Quiz.objects.filter(topic=informacni_topic, title__icontains='Single Choice Set').first()
            if quiz3:
                # Tento test obsahuje "Informační systémy", ale používá stejný H5P jako "Základy informatiky"
                # Možná by měl mít vlastní H5P soubor, ale zatím použijeme ZI-single-choice
                old_path = quiz3.h5p_path
                quiz3.h5p_path = 'h5p/ZI-single-choice/'
                quiz3.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opraven test: {quiz3.title}'))
                self.stdout.write(f'  {old_path} → {quiz3.h5p_path}')
                self.stdout.write(self.style.WARNING('  ⚠ POZOR: Tento test používá stejný H5P jako "Základy informatiky"'))
                self.stdout.write('     Měl by mít vlastní H5P soubor pro "Informační systémy"')
        
        self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Hotovo!'))

