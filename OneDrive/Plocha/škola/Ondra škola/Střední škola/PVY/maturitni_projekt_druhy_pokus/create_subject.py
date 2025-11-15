"""
Skript pro vytvoření předmětu "Programové vybavení".
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maturitni_projekt.settings.dev')
django.setup()

from subjects.models import Subject

print("=" * 70)
print("VYTVOŘENÍ PŘEDMĚTU 'PROGRAMOVÉ VYBAVENÍ'")
print("=" * 70)
print()

# Vytvořit předmět
subject, created = Subject.objects.get_or_create(
    slug='programove-vybaveni',
    defaults={
        'name': 'Programové vybavení',
        'description': 'Příprava k maturitě z předmětu Programové vybavení'
    }
)

if created:
    print(f"✓ Vytvořen předmět: {subject.name}")
    print(f"  Slug: {subject.slug}")
    print(f"  ID: {subject.id}")
else:
    print(f"✓ Předmět '{subject.name}' již existuje")
    print(f"  Slug: {subject.slug}")
    print(f"  ID: {subject.id}")

print()
print("=" * 70)

