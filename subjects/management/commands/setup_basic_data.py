"""
Management command pro vytvoření základní struktury dat (předmět, okruhy, materiály a testy).
Tento příkaz vytvoří kompletní strukturu včetně materiálů a testů.
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from materials.models import Material, MaterialType
from quizzes.models import Quiz
from accounts.models import User


class Command(BaseCommand):
    help = 'Vytvoří kompletní strukturu: předmět "Programové vybavení", 3 okruhy, materiály a testy'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("VYTVOŘENÍ ZÁKLADNÍ STRUKTURY")
        self.stdout.write("=" * 70)
        self.stdout.write()

        # 1. Vytvořit nebo získat předmět "Programové vybavení"
        subject, created = Subject.objects.get_or_create(
            slug='programove-vybaveni',
            defaults={
                'name': 'Programové vybavení',
                'description': 'Příprava k maturitě z předmětu Programové vybavení'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen předmět: {subject.name}"))
        else:
            self.stdout.write(f"✓ Použit existující předmět: {subject.name}")

        self.stdout.write()

        # 2. Definice okruhů
        topics_data = [
            {
                'slug': 'zaklady-informatiky',
                'name': 'Základy informatiky',
                'description': 'Pojem informatika, informace, data, signál, digitalizace, jednotky, číselné soustavy, kódování, přenos informací a datová komprese.',
                'order': 1
            },
            {
                'slug': 'programy-a-data',
                'name': 'Programy a data',
                'description': 'Programové a datové soubory. Systémové a aplikační programy, utility a speciální software. Programy a autorský zákon, softwarové licence. Instalace programů, zálohování programů a dat. Cloudová řešení, emulace a virtualizace.',
                'order': 2
            },
            {
                'slug': 'informacni-systemy-a-databazove-systemy',
                'name': 'Informační systémy a databázové systémy',
                'description': 'Informační systém, jeho komponenty, základní koncepce a rozdělení. Základní typy IS a příklady využití v praxi. Životní cyklus vývoje IS, nasazení a správa IS. Databázový systém, datový sklad, big data a data mining. Typy moderních databázových systémů, jejich charakteristické rysy a využití.',
                'order': 3
            }
        ]

        # 3. Vytvořit okruhy
        created_topics = []
        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                subject=subject,
                slug=topic_data['slug'],
                defaults={
                    'name': topic_data['name'],
                    'description': topic_data['description'],
                    'order': topic_data['order']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen okruh: {topic.name} (pořadí: {topic.order})"))
                created_topics.append(topic)
            else:
                self.stdout.write(f"✓ Použit existující okruh: {topic.name} (pořadí: {topic.order})")
                # Aktualizovat popis a pořadí, pokud se změnilo
                if topic.description != topic_data['description'] or topic.order != topic_data['order']:
                    topic.description = topic_data['description']
                    topic.order = topic_data['order']
                    topic.save()
                    self.stdout.write(f"  → Aktualizován popis a pořadí")

        self.stdout.write()
        
        # 4. Vytvořit materiály a testy pro každý okruh
        self.stdout.write("=" * 70)
        self.stdout.write("VYTVÁŘENÍ MATERIÁLŮ A TESTŮ")
        self.stdout.write("=" * 70)
        self.stdout.write()
        
        # Najít autora
        author = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not author:
            self.stdout.write(self.style.WARNING("⚠️  Není žádný uživatel v databázi. Materiály a testy budou vytvořeny bez autora."))
        
        # Základy informatiky
        zaklady_topic = Topic.objects.get(subject=subject, slug='zaklady-informatiky')
        
        # Materiál: Interactive Book
        material_zaklady, created = Material.objects.get_or_create(
            topic=zaklady_topic,
            title='Základy informatiky - Interactive Book',
            defaults={
                'description': 'Interaktivní kniha z oblasti základů informatiky.',
                'material_type': MaterialType.H5P,
                'author': author,
                'is_published': True,
                'h5p_path': 'h5p/ZI-interactive-book/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material_zaklady.title}"))
        
        # Test: Single Choice Set
        quiz_zaklady_single, created = Quiz.objects.get_or_create(
            topic=zaklady_topic,
            title='Základy informatiky - Single Choice Set',
            defaults={
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti základů informatiky.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/ZI-single-choice/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz_zaklady_single.title}"))
        
        # Programy a data
        programy_topic = Topic.objects.get(subject=subject, slug='programy-a-data')
        
        # Materiál: Interactive Book
        material_programy, created = Material.objects.get_or_create(
            topic=programy_topic,
            title='Programy a data - Interactive Book',
            defaults={
                'description': 'Interaktivní kniha z oblasti programů a dat.',
                'material_type': MaterialType.H5P,
                'author': author,
                'is_published': True,
                'h5p_path': 'h5p/PaD-interactive-book/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material_programy.title}"))
        
        # Test: Single Choice Set
        quiz_programy_single, created = Quiz.objects.get_or_create(
            topic=programy_topic,
            title='Programy a data - Single Choice Set',
            defaults={
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti programů a dat.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/PaD-single-choice-set/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz_programy_single.title}"))
        
        # Test: Question Set
        quiz_programy_question, created = Quiz.objects.get_or_create(
            topic=programy_topic,
            title='Programy a data - Question Set',
            defaults={
                'description': 'Soubor otázek z oblasti programů a dat.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/PaD-question-set/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz_programy_question.title}"))
        
        # Informační systémy a databázové systémy
        informacni_topic = Topic.objects.get(subject=subject, slug='informacni-systemy-a-databazove-systemy')
        
        # Materiál: Interactive Book
        material_informacni, created = Material.objects.get_or_create(
            topic=informacni_topic,
            title='Informační systémy a databázové systémy - Interactive Book',
            defaults={
                'description': 'Interaktivní kniha z oblasti informačních systémů a databázových systémů.',
                'material_type': MaterialType.H5P,
                'author': author,
                'is_published': True,
                'h5p_path': 'h5p/ISaDS-interactive-book/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material_informacni.title}"))
        
        # Test: Single Choice Set
        quiz_informacni_single, created = Quiz.objects.get_or_create(
            topic=informacni_topic,
            title='Informační systémy a databázové systémy - Single Choice Set',
            defaults={
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/ISaDS-single-choice-set/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz_informacni_single.title}"))
        
        # Test: Question Set
        quiz_informacni_question, created = Quiz.objects.get_or_create(
            topic=informacni_topic,
            title='Informační systémy a databázové systémy - Question Set',
            defaults={
                'description': 'Soubor otázek z oblasti informačních systémů a databázových systémů.',
                'author': author,
                'is_published': True,
                'passing_score': 60,
                'h5p_path': 'h5p/ISaDS-question-set/',
                'h5p_embed_code': None
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz_informacni_question.title}"))
        
        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("✓ HOTOVO! Kompletní struktura byla vytvořena."))
        self.stdout.write("=" * 70)
        self.stdout.write()
        self.stdout.write(f"Předmět: {subject.name}")
        self.stdout.write(f"Počet okruhů: {Topic.objects.filter(subject=subject).count()}")
        self.stdout.write()
        self.stdout.write("Vytvořené okruhy:")
        for topic in Topic.objects.filter(subject=subject).order_by('order'):
            materials_count = Material.objects.filter(topic=topic, is_published=True).count()
            quizzes_count = Quiz.objects.filter(topic=topic, is_published=True).count()
            self.stdout.write(f"  {topic.order}. {topic.name} ({materials_count} materiálů, {quizzes_count} testů)")
        self.stdout.write()
        self.stdout.write("POZNÁMKA: H5P soubory musí být v adresáři media/h5p/ s odpovídajícími názvy složek.")
        self.stdout.write()

