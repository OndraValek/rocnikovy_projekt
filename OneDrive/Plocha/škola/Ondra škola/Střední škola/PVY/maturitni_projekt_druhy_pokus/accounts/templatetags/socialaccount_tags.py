"""
Custom template tags pro bezpečné zpracování OAuth2 provider URLs.
"""
from django import template
from django.core.exceptions import MultipleObjectsReturned
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def safe_provider_login_url(context, provider):
    """
    Bezpečně získat URL pro OAuth2 přihlášení.
    Používá adapter, který automaticky řeší duplicity.
    Pokud dojde k chybě, vrátí "#".
    """
    try:
        request = context.get('request')
        if not request:
            return "#"
        
        # Použít adapter, který už má ochranu proti duplicitám
        from allauth.socialaccount.adapter import get_adapter
        adapter = get_adapter(request)
        
        # get_provider používá get_app, který už řeší duplicity
        provider_obj = adapter.get_provider(request, provider)
        if provider_obj:
            return reverse('socialaccount_login', args=[provider])
        return "#"
    except (MultipleObjectsReturned, Exception):
        # Pokud dojde k chybě, vrátit "#"
        # Tlačítko nebude funkční, ale stránka se načte bez chyby
        return "#"

