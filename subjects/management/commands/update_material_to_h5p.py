"""
Management command pro aktualizaci materiálu "Základy informatiky" na H5P.
"""
from django.core.management.base import BaseCommand
from materials.models import Material, MaterialType


class Command(BaseCommand):
    help = 'Aktualizuje materiál "Základy informatiky" na H5P typ'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("AKTUALIZACE MATERIÁLU 'ZÁKLADY INFORMATIKY' NA H5P")
        self.stdout.write("=" * 70)
        self.stdout.write()

        try:
            material = Material.objects.get(title='Základy informatiky')
            
            # H5P embed kód
            h5p_embed_code = """<iframe src="https://ondak.h5p.com/content/1292747373383202017/embed" aria-label="Základy informatiky - Interactive Book" width="1088" height="637" frameborder="0" allowfullscreen="allowfullscreen" allow="autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://ondak.h5p.com/js/h5p-resizer.js" charset="UTF-8"></script>"""
            
            # Aktualizovat materiál
            material.material_type = MaterialType.H5P
            material.h5p_embed_code = h5p_embed_code
            material.content = ''  # Vymazat textový obsah
            material.save()
            
            self.stdout.write(self.style.SUCCESS("✓ Materiál byl úspěšně aktualizován!"))
            self.stdout.write(f"Název: {material.title}")
            self.stdout.write(f"Typ: {material.get_material_type_display()}")
            self.stdout.write(f"URL: /materials/{material.id}/")
            self.stdout.write("=" * 70)
            
        except Material.DoesNotExist:
            self.stdout.write(self.style.ERROR("Materiál 'Základy informatiky' nebyl nalezen."))
            self.stdout.write("Spusťte nejdřív: python manage.py add_material_zaklady_informatiky")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Chyba: {e}"))
            import traceback
            traceback.print_exc()

