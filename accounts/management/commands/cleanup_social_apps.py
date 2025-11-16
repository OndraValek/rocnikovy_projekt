"""
Management command pro smazání všech Social Applications a vytvoření nových.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config


class Command(BaseCommand):
    help = 'Smaže všechny Social Applications a vytvoří nové z .env'

    def handle(self, *args, **options):
        # Smazat všechny existující Social Applications
        count = SocialApp.objects.all().count()
        SocialApp.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Smaženo {count} Social Applications'))
        
        # Získat nebo vytvořit Site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Maturitní projekt'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Vytvořen nový Site: {site.domain}'))
        else:
            self.stdout.write(f'Použit existující Site: {site.domain}')

        # Google
        google_client_id = config('GOOGLE_CLIENT_ID', default='')
        google_secret = config('GOOGLE_CLIENT_SECRET', default='')
        
        if google_client_id and google_secret and 'your-' not in google_client_id:
            google_app = SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id=google_client_id,
                secret=google_secret,
            )
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena Google Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Google OAuth2 není nakonfigurován'))

        # GitHub
        github_client_id = config('GITHUB_CLIENT_ID', default='')
        github_secret = config('GITHUB_CLIENT_SECRET', default='')
        
        if github_client_id and github_secret and 'your-' not in github_client_id:
            github_app = SocialApp.objects.create(
                provider='github',
                name='GitHub',
                client_id=github_client_id,
                secret=github_secret,
            )
            github_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena GitHub Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ GitHub OAuth2 není nakonfigurován'))

        # Microsoft
        microsoft_client_id = config('MICROSOFT_CLIENT_ID', default='')
        microsoft_secret = config('MICROSOFT_CLIENT_SECRET', default='')
        
        if microsoft_client_id and microsoft_secret and 'your-' not in microsoft_client_id:
            microsoft_app = SocialApp.objects.create(
                provider='microsoft',
                name='Microsoft',
                client_id=microsoft_client_id,
                secret=microsoft_secret,
            )
            microsoft_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena Microsoft Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Microsoft OAuth2 není nakonfigurován'))

        self.stdout.write(self.style.SUCCESS('\nHotovo! Všechny Social Applications byly vyčištěny a vytvořeny znovu.'))

