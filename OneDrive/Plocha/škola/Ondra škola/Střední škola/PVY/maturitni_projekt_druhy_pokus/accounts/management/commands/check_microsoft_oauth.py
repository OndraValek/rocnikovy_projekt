"""
Management command pro kontrolu Microsoft OAuth2 konfigurace.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config
from django.conf import settings


class Command(BaseCommand):
    help = 'Zkontroluje Microsoft OAuth2 konfiguraci'

    def handle(self, *args, **options):
        print("=" * 70)
        print("DIAGNOSTIKA MICROSOFT OAUTH2")
        print("=" * 70)
        print()

        # 1. Zkontrolovat Site domain
        print("1. DJANGO SITE DOMAIN:")
        print("-" * 70)
        site = Site.objects.get_current()
        print(f"   Domain: {site.domain}")
        print(f"   Name: {site.name}")
        if site.domain != "localhost:8000":
            print(f"   ⚠️  PROBLÉM: Domain by měl být 'localhost:8000'")
        else:
            print(f"   ✓ Domain je správně nastaven")
        print()

        # 2. Zkontrolovat SocialApp
        print("2. SOCIALAPP KONFIGURACE:")
        print("-" * 70)
        microsoft_apps = SocialApp.objects.filter(provider='microsoft')
        count = microsoft_apps.count()

        if count == 0:
            print("   ❌ CHYBA: Není vytvořena žádná Microsoft SocialApp!")
            print("   → Spusť: python manage.py create_social_apps")
        elif count > 1:
            print(f"   ⚠️  VAROVÁNÍ: Nalezeno {count} Microsoft SocialApp (měla by být jen 1)")
            for app in microsoft_apps:
                print(f"      - ID: {app.id}, Name: {app.name}, Client ID: {app.client_id[:20]}...")
        else:
            app = microsoft_apps.first()
            print(f"   ✓ Nalezena 1 Microsoft SocialApp")
            print(f"      ID: {app.id}")
            print(f"      Name: {app.name}")
            print(f"      Provider: {app.provider}")
            print(f"      Client ID: {app.client_id}")
            print(f"      Secret: {'✓ Nastaven' if app.secret else '❌ CHYBÍ'}")
            print(f"      Sites: {[s.domain for s in app.sites.all()]}")
            
            if site not in app.sites.all():
                print(f"      ⚠️  PROBLÉM: Site '{site.domain}' není přiřazen k SocialApp!")
            else:
                print(f"      ✓ Site je správně přiřazen")
        print()

        # 3. Zkontrolovat Environment Variables
        print("3. ENVIRONMENT VARIABLES:")
        print("-" * 70)
        microsoft_client_id = config('MICROSOFT_CLIENT_ID', default='')
        microsoft_client_secret = config('MICROSOFT_CLIENT_SECRET', default='')

        if not microsoft_client_id:
            print("   ❌ CHYBA: MICROSOFT_CLIENT_ID není nastaven v .env")
        else:
            print(f"   ✓ MICROSOFT_CLIENT_ID: {microsoft_client_id[:20]}...")
            
        if not microsoft_client_secret:
            print("   ❌ CHYBA: MICROSOFT_CLIENT_SECRET není nastaven v .env")
        else:
            print(f"   ✓ MICROSOFT_CLIENT_SECRET: {'✓ Nastaven' if microsoft_client_secret else '❌ CHYBÍ'}")

        # Zkontrolovat, jestli se shodují s SocialApp
        if microsoft_apps.exists():
            app = microsoft_apps.first()
            if app.client_id != microsoft_client_id:
                print(f"   ⚠️  VAROVÁNÍ: Client ID v SocialApp se neshoduje s .env")
            if app.secret != microsoft_client_secret:
                print(f"   ⚠️  VAROVÁNÍ: Secret v SocialApp se neshoduje s .env")
        print()

        # 4. Vygenerovat očekávaný redirect URI
        print("4. OČEKÁVANÝ REDIRECT URI:")
        print("-" * 70)
        expected_redirect = f"http://{site.domain}/accounts/microsoft/login/callback/"
        print(f"   {expected_redirect}")
        print()
        print("   ⚠️  ZKONTROLUJ V AZURE PORTAL:")
        print("   1. Jdi na: https://portal.azure.com/")
        print("   2. Azure Active Directory → App registrations")
        print("   3. Klikni na tvou aplikaci")
        print("   4. Authentication → Redirect URIs")
        print(f"   5. MUSÍ tam být: {expected_redirect}")
        print()

        # 5. Zkontrolovat Settings
        print("5. DJANGO SETTINGS:")
        print("-" * 70)
        microsoft_provider = settings.SOCIALACCOUNT_PROVIDERS.get('microsoft', {})
        tenant = microsoft_provider.get('TENANT', 'NENÍ NASTAVEN')
        print(f"   TENANT: {tenant}")
        if tenant != 'common':
            print(f"   ⚠️  PROBLÉM: TENANT by měl být 'common' pro multi-tenant")
        else:
            print(f"   ✓ TENANT je správně nastaven na 'common'")
        print()

        # 6. Shrnutí
        print("=" * 70)
        print("SHRNUTÍ:")
        print("=" * 70)
        print()

        issues = []

        if site.domain != "localhost:8000":
            issues.append("Site domain není 'localhost:8000'")

        if microsoft_apps.count() == 0:
            issues.append("Není vytvořena Microsoft SocialApp")
        elif microsoft_apps.count() > 1:
            issues.append("Jsou duplicitní Microsoft SocialApp")

        if not microsoft_client_id:
            issues.append("MICROSOFT_CLIENT_ID není v .env")

        if not microsoft_client_secret:
            issues.append("MICROSOFT_CLIENT_SECRET není v .env")

        if tenant != 'common':
            issues.append("TENANT není nastaven na 'common'")

        if issues:
            print("   ❌ NALEZENY PROBLÉMY:")
            for i, issue in enumerate(issues, 1):
                print(f"      {i}. {issue}")
            print()
            print("   → Oprav tyto problémy a spusť diagnostiku znovu")
        else:
            print("   ✓ Všechny základní kontroly prošly")
            print()
            print("   ⚠️  Pokud to stále nefunguje:")
            print("      1. Zkontroluj Azure Portal → Redirect URIs")
            print("      2. Zkontroluj Azure Portal → Supported account types")
            print("      3. Zkontroluj Azure Portal → Client Secret (není expirovaný?)")
            print("      4. Restartuj Django server")
            print("      5. Zkus přistupovat přes http://localhost:8000 (ne 127.0.0.1)")

        print()
        print("=" * 70)

