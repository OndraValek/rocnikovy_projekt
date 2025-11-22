"""
Management command pro vytvoření základních inicializačních dat.

Vytvoří:
- Předmět "Programové vybavení"
- 3 základní maturitní okruhy:
  1. Základy informatiky
  2. Programy a data
  3. Informační systémy a databázové systémy
- Pro okruh "Základy informatiky":
  - H5P materiál "Základy informatiky"
  - 2 testy (Single Choice Set, Question Set)
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from materials.models import Material, MaterialType
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Vytvoří základní inicializační data: předmět "Programové vybavení" a 3 maturitní okruhy'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("VYTVOŘENÍ ZÁKLADNÍCH INICIALIZAČNÍCH DAT")
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

        # 4. Vytvořit materiál a testy pro okruh "Základy informatiky"
        zaklady_topic = Topic.objects.get(subject=subject, slug='zaklady-informatiky')
        
        self.stdout.write("=" * 70)
        self.stdout.write("VYTVÁŘENÍ MATERIÁLŮ A TESTŮ PRO 'ZÁKLADY INFORMATIKY'")
        self.stdout.write("=" * 70)
        self.stdout.write()

        # 4.1. Vytvořit H5P materiál
        h5p_embed_code = """<iframe src="https://ondak.h5p.com/content/1292747373383202017/embed" aria-label="Základy informatiky - Interactive Book" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>"""

        material, created = Material.objects.get_or_create(
            topic=zaklady_topic,
            title='Základy informatiky',
            defaults={
                'material_type': MaterialType.H5P,
                'description': 'Pojem informatika, informace, data, signál (analogový, digitální), digitalizace. Jednotky v informatice. Číselné soustavy a jejich převody. Princip kódování informací, kódování znaků, reprezentace čísel v počítači. Přenos informací a princip datové komprese.',
                'h5p_embed_code': h5p_embed_code,
                'is_published': True,
                'order': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material.title}"))
        else:
            material.material_type = MaterialType.H5P
            material.h5p_embed_code = h5p_embed_code
            material.content = ''
            material.description = 'Pojem informatika, informace, data, signál (analogový, digitální), digitalizace. Jednotky v informatice. Číselné soustavy a jejich převody. Princip kódování informací, kódování znaků, reprezentace čísel v počítači. Přenos informací a princip datové komprese.'
            material.is_published = True
            material.order = 1
            material.save()
            self.stdout.write(f"✓ Aktualizován materiál: {material.title}")

        # 4.2. Vytvořit testy
        quizzes_data = [
            {
                'title': 'Základy informatiky - Single Choice Set',
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti základů informatiky.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747373384939787/embed" aria-label="Základy informatiky - Single Choice Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
            },
            {
                'title': 'Základy informatiky - Question Set',
                'description': 'Soubor otázek z oblasti základů informatiky.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747373384268647/embed" aria-label="Základy informatiky - Question Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
            }
        ]

        created_quizzes = 0
        updated_quizzes = 0

        for quiz_data in quizzes_data:
            quiz, created = Quiz.objects.get_or_create(
                topic=zaklady_topic,
                title=quiz_data['title'],
                defaults={
                    'description': quiz_data['description'],
                    'h5p_embed_code': quiz_data['h5p_embed_code'],
                    'is_published': True,
                    'max_attempts': 3,
                    'passing_score': 60,
                }
            )

            if created:
                created_quizzes += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz.title}"))
            else:
                quiz.description = quiz_data['description']
                quiz.h5p_embed_code = quiz_data['h5p_embed_code']
                quiz.is_published = True
                quiz.max_attempts = 3
                quiz.passing_score = 60
                quiz.save()
                updated_quizzes += 1
                self.stdout.write(f"✓ Aktualizován test: {quiz.title}")

        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("✓ HOTOVO! Základní inicializační data byla úspěšně vytvořena."))
        self.stdout.write("=" * 70)
        self.stdout.write()
        self.stdout.write(f"Předmět: {subject.name}")
        self.stdout.write(f"Počet okruhů: {Topic.objects.filter(subject=subject).count()}")
        self.stdout.write()
        self.stdout.write("Vytvořené okruhy:")
        for topic in Topic.objects.filter(subject=subject).order_by('order'):
            self.stdout.write(f"  {topic.order}. {topic.name}")
        self.stdout.write()
        self.stdout.write(f"Pro okruh 'Základy informatiky':")
        self.stdout.write(f"  - Materiál: {material.title}")
        self.stdout.write(f"  - Testy: {created_quizzes + updated_quizzes} (vytvořeno: {created_quizzes}, aktualizováno: {updated_quizzes})")
        self.stdout.write()
        self.stdout.write("=" * 70)

