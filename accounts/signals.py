"""
Signals pro zachycení OAuth2 událostí a automatické nastavení is_staff.
"""
import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.signals import pre_social_login, social_account_added
from .models import User

logger = logging.getLogger('accounts')

@receiver(pre_social_login)
def pre_social_login_handler(sender, request, sociallogin, **kwargs):
    """Handler pro pre_social_login signal."""
    logger.info("=" * 70)
    logger.info("PRE_SOCIAL_LOGIN SIGNAL")
    logger.info(f"Provider: {sociallogin.account.provider}")
    logger.info(f"Is existing: {sociallogin.is_existing}")
    logger.info("=" * 70)

@receiver(social_account_added)
def social_account_added_handler(sender, request, sociallogin, **kwargs):
    """Handler pro social_account_added signal."""
    logger.info("=" * 70)
    logger.info("SOCIAL_ACCOUNT_ADDED SIGNAL")
    logger.info(f"Provider: {sociallogin.account.provider}")
    logger.info("=" * 70)

@receiver(user_signed_up)
def user_signed_up_handler(sender, request, user, **kwargs):
    """Handler pro user_signed_up signal."""
    logger.info("=" * 70)
    logger.info("USER_SIGNED_UP SIGNAL")
    logger.info(f"User: {user.email}, username: {user.username}")
    logger.info("=" * 70)

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """Handler pro user_logged_in signal."""
    logger.info("=" * 70)
    logger.info("USER_LOGGED_IN SIGNAL")
    logger.info(f"User: {user.email}, username: {user.username}")
    logger.info("=" * 70)
    
    # Zkontrolovat a opravit is_staff a is_active status při přihlášení
    # Toto zajistí, že i existující uživatelé budou mít správný is_staff a is_active status
    needs_update = False
    update_fields = {}
    
    if user.role in [User.Role.TEACHER, User.Role.ADMIN] or user.is_superuser:
        if not user.is_staff:
            user.is_staff = True
            update_fields['is_staff'] = True
            needs_update = True
            logger.info(f"Nastaveno is_staff=True pro uživatele {user.email} (role: {user.role})")
        if not user.is_active:
            user.is_active = True
            update_fields['is_active'] = True
            needs_update = True
            logger.info(f"Nastaveno is_active=True pro uživatele {user.email} (role: {user.role})")
    elif user.role == User.Role.STUDENT and not user.is_superuser:
        if user.is_staff:
            user.is_staff = False
            update_fields['is_staff'] = False
            needs_update = True
            logger.info(f"Nastaveno is_staff=False pro uživatele {user.email} (role: {user.role})")
    
    if needs_update:
        # Uložit změnu bez spuštění dalších signalů (aby se zabránilo nekonečné smyčce)
        User.objects.filter(pk=user.pk).update(**update_fields)


@receiver(pre_save, sender=User)
def set_staff_status(sender, instance, **kwargs):
    """
    Automaticky nastavit is_staff=True a is_active=True pro učitele a adminy.
    Umožňuje přístup do Wagtail adminu.
    """
    if instance.role in [User.Role.TEACHER, User.Role.ADMIN] or instance.is_superuser:
        instance.is_staff = True
        instance.is_active = True  # Učitelé a admini musí být aktivní
    elif instance.role == User.Role.STUDENT and not instance.is_superuser:
        # Studenti nemají přístup do adminu (pokud nejsou superuser)
        instance.is_staff = False
        # Studenti mohou být aktivní (pro přístup do aplikace)
