"""
Management command pro přidání materiálu "Základy informatiky" do databáze.
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from materials.models import Material, MaterialType


class Command(BaseCommand):
    help = 'Přidá materiál "Základy informatiky" do databáze'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("PŘIDÁNÍ MATERIÁLU 'ZÁKLADY INFORMATIKY'")
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
            slug='zaklady-informatiky',
            defaults={
                'name': 'Základy informatiky',
                'description': 'Pojem informatika, informace, data, signál, digitalizace, jednotky, číselné soustavy, kódování, přenos informací a datová komprese.',
                'order': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen okruh: {topic.name}"))
        else:
            self.stdout.write(f"✓ Použit existující okruh: {topic.name}")

        # 3. H5P embed kód
        h5p_embed_code = """<iframe src="https://ondak.h5p.com/content/1292747373383202017/embed" aria-label="Základy informatiky - Interactive Book" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>"""

        # 4. Vytvořit nebo aktualizovat materiál
        material, created = Material.objects.get_or_create(
            topic=topic,
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
            # Aktualizovat obsah, pokud materiál již existuje
            material.material_type = MaterialType.H5P
            material.h5p_embed_code = h5p_embed_code
            material.content = ''  # Vymazat textový obsah
            material.description = 'Pojem informatika, informace, data, signál (analogový, digitální), digitalizace. Jednotky v informatice. Číselné soustavy a jejich převody. Princip kódování informací, kódování znaků, reprezentace čísel v počítači. Přenos informací a princip datové komprese.'
            material.is_published = True
            material.order = 1
            material.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Aktualizován materiál: {material.title}"))

        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("✓ Hotovo! Materiál byl úspěšně přidán/aktualizován."))
        self.stdout.write()
        self.stdout.write(f"Předmět: {subject.name}")
        self.stdout.write(f"Okruh: {topic.name}")
        self.stdout.write(f"Materiál: {material.title}")
        self.stdout.write(f"Typ: {material.get_material_type_display()}")
        self.stdout.write(f"URL: /materials/{material.id}/")
        self.stdout.write("=" * 70)

