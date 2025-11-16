"""
Management command pro přidání H5P testů k okruhu "Základy informatiky".
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from quizzes.models import Quiz


class Command(BaseCommand):
    help = 'Přidá H5P testy k okruhu "Základy informatiky"'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("PŘIDÁNÍ H5P TESTŮ K OKRUHU 'ZÁKLADY INFORMATIKY'")
        self.stdout.write("=" * 70)
        self.stdout.write()

        # 1. Najít okruh "Základy informatiky"
        try:
            topic = Topic.objects.get(slug='zaklady-informatiky')
            self.stdout.write(f"✓ Nalezen okruh: {topic.name}")
        except Topic.DoesNotExist:
            self.stdout.write(self.style.ERROR("Okruh 'Základy informatiky' nebyl nalezen."))
            self.stdout.write("Spusťte nejdřív: python manage.py add_material_zaklady_informatiky")
            return

        # 2. H5P embed kódy pro testy
        quizzes_data = [
            {
                'title': 'Základy informatiky - Single Choice Set',
                'description': 'Test s jednoduchými výběrovými otázkami z oblasti základů informatiky.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747373384939787/embed" aria-label="Základy informatiky - Single Choice Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
                'order': 1
            },
            {
                'title': 'Základy informatiky - Question Set',
                'description': 'Soubor otázek z oblasti základů informatiky.',
                'h5p_embed_code': '<iframe src="https://ondak.h5p.com/content/1292747373384268647/embed" aria-label="Základy informatiky - Question Set" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>',
                'order': 2
            }
        ]

        # 3. Vytvořit nebo aktualizovat testy
        created_count = 0
        updated_count = 0

        for quiz_data in quizzes_data:
            quiz, created = Quiz.objects.get_or_create(
                topic=topic,
                title=quiz_data['title'],
                defaults={
                    'description': quiz_data['description'],
                    'h5p_embed_code': quiz_data['h5p_embed_code'],
                    'is_published': True,
                    'max_attempts': 3,  # Povolit 3 pokusy
                    'passing_score': 60,  # 60% pro úspěch
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen test: {quiz.title}"))
            else:
                # Aktualizovat, pokud již existuje
                quiz.description = quiz_data['description']
                quiz.h5p_embed_code = quiz_data['h5p_embed_code']
                quiz.is_published = True
                quiz.max_attempts = 3
                quiz.passing_score = 60
                quiz.save()
                updated_count += 1
                self.stdout.write(f"✓ Aktualizován test: {quiz.title}")

        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS(f"✓ Hotovo! Vytvořeno: {created_count}, Aktualizováno: {updated_count}"))
        self.stdout.write()
        self.stdout.write(f"Okruh: {topic.name}")
        self.stdout.write(f"Předmět: {topic.subject.name}")
        self.stdout.write("=" * 70)

