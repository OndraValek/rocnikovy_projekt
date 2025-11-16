"""
Signals pro zachycení OAuth2 událostí.
"""
import logging
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.signals import pre_social_login, social_account_added

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
