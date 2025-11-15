"""
Custom adapter pro django-allauth pro podporu custom User modelu.
"""
import logging
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

logger = logging.getLogger('accounts')


class AccountAdapter(DefaultAccountAdapter):
    """Adapter pro běžné účty."""
    
    def is_open_for_signup(self, request):
        """Povolit registraci."""
        return True
    
    def save_user(self, request, user, form, commit=True):
        """Uložit uživatele s custom poli."""
        user = super().save_user(request, user, form, commit=False)
        
        # Nastavit email jako username, pokud je potřeba
        if not user.username:
            user.username = user.email
        
        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Adapter pro sociální účty (OAuth2)."""
    
    def is_open_for_signup(self, request, sociallogin):
        """Povolit registraci přes OAuth2."""
        return True
    
    def populate_user(self, request, sociallogin, data):
        """Naplnit uživatele daty z OAuth2 poskytovatele."""
        logger.info("=" * 70)
        logger.info("POPULATE_USER CALLED")
        logger.info(f"Provider: {sociallogin.account.provider}")
        logger.info(f"Data: {data}")
        logger.info(f"Extra data: {sociallogin.account.extra_data}")
        logger.info("=" * 70)
        
        try:
            user = super().populate_user(request, sociallogin, data)
            logger.info(f"Super().populate_user returned: email={user.email}, username={user.username}")
        except Exception as e:
            logger.error(f"ERROR in super().populate_user: {e}", exc_info=True)
            raise
        
        # Microsoft může posílat data jinak - zkontrolovat extra_data
        extra_data = sociallogin.account.extra_data
        
        # Získat email z různých zdrojů
        email = user.email or data.get('email') or extra_data.get('email') or extra_data.get('mail') or extra_data.get('userPrincipalName')
        if email:
            user.email = email
            logger.debug(f"Email nastaven: {email}")
        
        # Pokud uživatel nemá username, použít email nebo vygenerovat
        if not user.username:
            if email:
                # Použít email jako username (bez @ a domény)
                username = email.split('@')[0]
                # Zajistit unikátnost
                from accounts.models import User
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username
                logger.debug(f"Username vygenerován: {username}")
            else:
                user.username = f"user_{sociallogin.account.uid}"
                logger.debug(f"Username vygenerován z UID: {user.username}")
        
        # Naplnit jméno a příjmení z OAuth2 dat
        # Microsoft může používat 'givenName' a 'surname' nebo 'name'
        first_name = data.get('first_name') or extra_data.get('givenName') or extra_data.get('name', '').split()[0] if extra_data.get('name') else None
        last_name = data.get('last_name') or extra_data.get('surname') or ' '.join(extra_data.get('name', '').split()[1:]) if extra_data.get('name') and len(extra_data.get('name', '').split()) > 1 else None
        
        if first_name and not user.first_name:
            user.first_name = first_name
            logger.debug(f"First name nastaven: {first_name}")
        if last_name and not user.last_name:
            user.last_name = last_name
            logger.debug(f"Last name nastaven: {last_name}")
        
        logger.info(f"Final user before return: email={user.email}, username={user.username}, first_name={user.first_name}, last_name={user.last_name}")
        
        # Zajistit, že máme email a username
        if not user.email:
            logger.error("USER NEMÁ EMAIL! To je problém!")
        if not user.username:
            logger.error("USER NEMÁ USERNAME! To je problém!")
        
        logger.info("=" * 70)
        return user
    
    def pre_social_login(self, request, sociallogin):
        """Před přihlášením přes OAuth2."""
        logger.info("=" * 70)
        logger.info("PRE_SOCIAL_LOGIN CALLED")
        logger.info(f"Provider: {sociallogin.account.provider}")
        logger.info(f"Is existing: {sociallogin.is_existing}")
        logger.info(f"Extra data: {sociallogin.account.extra_data}")
        logger.info("=" * 70)
        
        # Pokud už existuje uživatel s tímto emailem, připojit k němu sociální účet
        if sociallogin.is_existing:
            logger.info("Social login is existing, skipping email lookup")
            return
        
        # Zkusit získat email z různých zdrojů (Microsoft může používat různé klíče)
        extra_data = sociallogin.account.extra_data
        email = extra_data.get('email') or extra_data.get('mail') or extra_data.get('userPrincipalName')
        
        logger.info(f"Extracted email: {email}")
        
        if email:
            from accounts.models import User
            try:
                user = User.objects.get(email=email)
                logger.info(f"Nalezen existující uživatel s emailem {email}, připojuji sociální účet")
                sociallogin.connect(request, user)
                logger.info("Sociální účet připojen")
            except User.DoesNotExist:
                logger.info(f"Uživatel s emailem {email} neexistuje, bude vytvořen nový")
            except User.MultipleObjectsReturned:
                logger.warning(f"Nalezeno více uživatelů s emailem {email}, použiji prvního")
                user = User.objects.filter(email=email).first()
                if user:
                    sociallogin.connect(request, user)
                    logger.info("Sociální účet připojen k prvnímu uživateli")
        else:
            logger.warning("Email nebyl nalezen v extra_data")
        
        logger.info("=" * 70)
    
    def get_app(self, request, provider, client_id=None):
        """
        Získat SocialApp pro poskytovatele.
        Pokud jsou duplicity, použije první aplikaci a automaticky opraví duplicity.
        """
        from allauth.socialaccount.models import SocialApp
        from django.core.exceptions import MultipleObjectsReturned
        from django.contrib.sites.models import Site
        
        # Nejdřív zkontrolovat, jestli nejsou duplicity
        apps = SocialApp.objects.filter(provider=provider)
        count = apps.count()
        
        if count > 1:
            # Jsou duplicity - opravit je
            first_app = apps.first()
            # Smazat ostatní
            apps.exclude(id=first_app.id).delete()
            # Ujistit se, že má správný site
            site = Site.objects.get_current()
            if site not in first_app.sites.all():
                first_app.sites.add(site)
            return first_app
        elif count == 1:
            # Je jen jedna aplikace - použít ji
            app = apps.first()
            site = Site.objects.get_current()
            if site not in app.sites.all():
                app.sites.add(site)
            return app
        else:
            # Žádná aplikace - použít původní logiku
            try:
                return super().get_app(request, provider, client_id)
            except MultipleObjectsReturned:
                # Pokud se to stalo, znovu zkontrolovat a opravit
                apps = SocialApp.objects.filter(provider=provider)
                if apps.count() > 1:
                    first_app = apps.first()
                    apps.exclude(id=first_app.id).delete()
                    site = Site.objects.get_current()
                    if site not in first_app.sites.all():
                        first_app.sites.add(site)
                    return first_app
                raise

