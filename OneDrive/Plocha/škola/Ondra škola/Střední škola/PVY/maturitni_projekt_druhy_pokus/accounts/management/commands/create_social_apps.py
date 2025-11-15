"""
Management command pro vytvoření Social Applications pro OAuth2.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config


class Command(BaseCommand):
    help = 'Vytvoří Social Applications pro OAuth2 poskytovatele (Google, GitHub, Microsoft)'

    def handle(self, *args, **options):
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
        
        if google_client_id and google_secret:
            # Smazat všechny existující Google aplikace pro tento site
            SocialApp.objects.filter(provider='google').delete()
            # Vytvořit novou
            google_app = SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id=google_client_id,
                secret=google_secret,
            )
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena Google Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Google OAuth2 není nakonfigurován (chybí GOOGLE_CLIENT_ID nebo GOOGLE_CLIENT_SECRET)'))

        # GitHub
        github_client_id = config('GITHUB_CLIENT_ID', default='')
        github_secret = config('GITHUB_CLIENT_SECRET', default='')
        
        if github_client_id and github_secret:
            # Smazat všechny existující GitHub aplikace
            SocialApp.objects.filter(provider='github').delete()
            # Vytvořit novou
            github_app = SocialApp.objects.create(
                provider='github',
                name='GitHub',
                client_id=github_client_id,
                secret=github_secret,
            )
            github_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena GitHub Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ GitHub OAuth2 není nakonfigurován (chybí GITHUB_CLIENT_ID nebo GITHUB_CLIENT_SECRET)'))

        # Microsoft
        microsoft_client_id = config('MICROSOFT_CLIENT_ID', default='')
        microsoft_secret = config('MICROSOFT_CLIENT_SECRET', default='')
        
        if microsoft_client_id and microsoft_secret:
            # Smazat všechny existující Microsoft aplikace
            SocialApp.objects.filter(provider='microsoft').delete()
            # Vytvořit novou
            microsoft_app = SocialApp.objects.create(
                provider='microsoft',
                name='Microsoft',
                client_id=microsoft_client_id,
                secret=microsoft_secret,
            )
            microsoft_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('✓ Vytvořena Microsoft Social Application'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Microsoft OAuth2 není nakonfigurován (chybí MICROSOFT_CLIENT_ID nebo MICROSOFT_CLIENT_SECRET)'))

        self.stdout.write(self.style.SUCCESS('\nHotovo! Social Applications byly vytvořeny/aktualizovány.'))

