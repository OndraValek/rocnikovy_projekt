"""
Management command pro přidání okruhu "Informační systémy a databázové systémy" s H5P materiálem a testy.
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from materials.models import Material, MaterialType
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Přidá okruh "Informační systémy a databázové systémy" s H5P materiálem a testy'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("PŘIDÁNÍ OKRUHU 'INFORMAČNÍ SYSTÉMY A DATABÁZOVÉ SYSTÉMY' S H5P OBSAHEM")
        self.stdout.write("=" * 70)
        self.stdout.write()

        # 1. Získat nebo vytvořit předmět
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

        # 2. Získat nebo vytvořit okruh
        topic, created = Topic.objects.get_or_create(
            subject=subject,
            slug='informacni-systemy-a-databazove-systemy',
            defaults={
                'name': 'Informační systémy a databázové systémy',
                'description': 'Informační systém, jeho komponenty, základní koncepce a rozdělení. Základní typy IS a příklady využití v praxi. Životní cyklus vývoje IS, nasazení a správa IS. Databázový systém, datový sklad, big data a data mining. Typy moderních databázových systémů, jejich charakteristické rysy a využití.',
                'order': 3
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen okruh: {topic.name}"))
        else:
            self.stdout.write(f"✓ Použit existující okruh: {topic.name}")

        # 3. H5P embed kód pro materiál
        h5p_embed_code_material = """<iframe src="https://ondak.h5p.com/content/1292747413837027327/embed" aria-label="Informační systémy a databázové systémy - Interactive Book" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>"""

        # 4. Vytvořit nebo aktualizovat materiál
        material, created = Material.objects.get_or_create(
            topic=topic,
            title='Informační systémy a databázové systémy',
            defaults={
                'material_type': MaterialType.H5P,
                'description': 'Informační systém, jeho komponenty, základní koncepce a rozdělení. Základní typy IS a příklady využití v praxi. Životní cyklus vývoje IS, nasazení a správa IS. Databázový systém, datový sklad, big data a data mining. Typy moderních databázových systémů, jejich charakteristické rysy a využití.',
                'h5p_embed_code': h5p_embed_code_material,
                'is_published': True,
                'order': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material.title}"))
        else:
            material.material_type = MaterialType.H5P
            material.h5p_embed_code = h5p_embed_code_material
            material.content = ''
            material.description = 'Informační systém, jeho komponenty, základní koncepce a rozdělení. Základní typy IS a příklady využití v praxi. Životní cyklus vývoje IS, nasazení a správa IS. Databázový systém, datový sklad, big data a data mining. Typy moderních databázových systémů, jejich charakteristické rysy a využití.'
            material.is_published = True
            material.order = 1
            material.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Aktualizován materiál: {material.title}"))

        # 5. H5P embed kódy pro testy
        quizzes_data = [
            {
                'title': 'Informační systémy a databázové systémy - Question Set',
                'description': 'Soubor otázek z oblasti informačních systémů a databázových systémů.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747413838507927/embed" aria-label="Informační systémy a databázové systémy - Question Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
                'order': 1
            },
            {
                'title': 'Informační systémy a databázové systémy - Single Choice Set',
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti informačních systémů a databázových systémů.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747413839037997/embed" aria-label="Informační systémy a databázové systémy - Single Choice Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
                'order': 2
            }
        ]

        # 6. Vytvořit nebo aktualizovat testy
        created_quizzes = 0
        updated_quizzes = 0

        for quiz_data in quizzes_data:
            quiz, created = Quiz.objects.get_or_create(
                topic=topic,
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
        self.stdout.write(self.style.SUCCESS("✓ Hotovo! Okruh byl úspěšně přidán/aktualizován."))
        self.stdout.write()
        self.stdout.write(f"Předmět: {subject.name}")
        self.stdout.write(f"Okruh: {topic.name}")
        self.stdout.write(f"Materiál: {material.title}")
        self.stdout.write(f"Testy: Vytvořeno {created_quizzes}, Aktualizováno {updated_quizzes}")
        self.stdout.write("=" * 70)

