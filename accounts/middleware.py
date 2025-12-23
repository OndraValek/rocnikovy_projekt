"""
Middleware pro zachycení OAuth2 callback požadavků a automatické nastavení is_staff.
"""
import logging
from .models import User

logger = logging.getLogger('accounts')

class OAuth2LoggingMiddleware:
    """Middleware pro logování OAuth2 callback požadavků."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Zaznamenat Microsoft callback
        if '/accounts/microsoft/login/callback/' in request.path:
            logger.info("=" * 70)
            logger.info("MICROSOFT CALLBACK REQUEST")
            logger.info(f"Path: {request.path}")
            logger.info(f"GET params: {request.GET}")
            logger.info(f"Method: {request.method}")
            logger.info("=" * 70)
        
        response = self.get_response(request)
        
        # Zaznamenat odpověď
        if '/accounts/microsoft/login/callback/' in request.path:
            logger.info("=" * 70)
            logger.info("MICROSOFT CALLBACK RESPONSE")
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Location header: {response.get('Location', 'N/A')}")
            logger.info("=" * 70)
        
        return response


class StaffStatusMiddleware:
    """
    Middleware pro automatické nastavení is_staff pro učitele a adminy.
    Zajišťuje přístup do Wagtail adminu na základě role.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pokud je uživatel přihlášen, zkontrolovat a nastavit is_staff
        if request.user.is_authenticated:
            user = request.user
            # Zkontrolovat, jestli má uživatel správnou roli
            if hasattr(user, 'role'):
                # Pro Wagtail admin - vždy nastavit is_staff podle role
                should_be_staff = (
                    user.role in [User.Role.TEACHER, User.Role.ADMIN] or 
                    user.is_superuser
                )
                
                # VŽDY nastavit is_staff a is_active v paměti podle role (pro tento request)
                # Toto je kritické pro Wagtail, který kontroluje oprávnění
                if should_be_staff:
                    # Nastavit přímo v objektu uživatele (v paměti) - použít __dict__ pro přímý přístup
                    user.__dict__['is_staff'] = True
                    user.__dict__['is_active'] = True
                    # Také nastavit pomocí setattr pro jistotu
                    setattr(user, 'is_staff', True)
                    setattr(user, 'is_active', True)
                    
                    # Pokud není nastaveno v databázi, uložit
                    try:
                        db_user = User.objects.get(pk=user.pk)
                        needs_update = False
                        if not db_user.is_staff:
                            logger.info(f"Middleware: Ukládám is_staff=True pro {user.email} (role: {user.role})")
                            needs_update = True
                        if not db_user.is_active:
                            logger.info(f"Middleware: Ukládám is_active=True pro {user.email} (role: {user.role})")
                            needs_update = True
                        if needs_update:
                            User.objects.filter(pk=user.pk).update(is_staff=True, is_active=True)
                    except User.DoesNotExist:
                        pass
                elif user.role == User.Role.STUDENT and not user.is_superuser:
                    user.__dict__['is_staff'] = False
                    setattr(user, 'is_staff', False)
                    # Studenti mohou být aktivní (pro přístup do aplikace)
                    # Pokud je nastaveno v databázi, opravit
                    if User.objects.filter(pk=user.pk, is_staff=True).exists():
                        logger.info(f"Middleware: Ukládám is_staff=False pro {user.email} (role: {user.role})")
                        User.objects.filter(pk=user.pk).update(is_staff=False)
        
        response = self.get_response(request)
        return response

