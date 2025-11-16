"""
Management command pro opravu duplicitních Social Applications.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Opraví duplicitní Social Applications - smaže duplicity a ponechá pouze jednu pro každého poskytovatele'

    def handle(self, *args, **options):
        try:
            site = Site.objects.get_current()
        except Site.DoesNotExist:
            # Pokud Site neexistuje, vytvořit ho
            site, created = Site.objects.get_or_create(
                id=1,
                defaults={
                    'domain': 'localhost:8000',
                    'name': 'Maturitní projekt'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Vytvořen nový Site: {site.domain}'))
        
        providers = ['google', 'github', 'microsoft']
        
        for provider in providers:
            try:
                apps = SocialApp.objects.filter(provider=provider)
                count = apps.count()
                
                if count > 1:
                    self.stdout.write(self.style.WARNING(f'Našel jsem {count} aplikací pro {provider}'))
                    
                    # Ponechat první a smazat ostatní
                    first_app = apps.first()
                    deleted_count = apps.exclude(id=first_app.id).delete()[0]
                    self.stdout.write(f'  Smazáno {deleted_count} duplicitních aplikací')
                    
                    # Ujistit se, že první má správný site
                    if site not in first_app.sites.all():
                        first_app.sites.add(site)
                        self.stdout.write(f'  Přidán Site k aplikaci')
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ Opraveno - ponechána jedna aplikace pro {provider}'))
                elif count == 1:
                    app = apps.first()
                    if site not in app.sites.all():
                        app.sites.add(site)
                        self.stdout.write(f'  Přidán Site k aplikaci')
                    self.stdout.write(self.style.SUCCESS(f'✓ {provider}: OK (1 aplikace)'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ {provider}: Žádná aplikace'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Chyba při zpracování {provider}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nHotovo! Duplicity byly opraveny.'))

