"""
Vlastní backend autentizace pro automatické nastavení is_staff podle role.
"""
from django.contrib.auth.backends import ModelBackend
from .models import User


class RoleBasedStaffBackend(ModelBackend):
    """
    Backend autentizace, který automaticky nastaví is_staff na základě role.
    """
    
    def get_user(self, user_id):
        """Získat uživatele a automaticky nastavit is_staff."""
        try:
            user = User.objects.get(pk=user_id)
            # Automaticky nastavit is_staff podle role
            if user.role in [User.Role.TEACHER, User.Role.ADMIN] or user.is_superuser:
                # Nastavit v paměti
                user.is_staff = True
                user.is_active = True
                # Uložit do databáze, pokud není nastaveno
                if not User.objects.filter(pk=user_id, is_staff=True, is_active=True).exists():
                    User.objects.filter(pk=user_id).update(is_staff=True, is_active=True)
            elif user.role == User.Role.STUDENT and not user.is_superuser:
                user.is_staff = False
                if User.objects.filter(pk=user_id, is_staff=True).exists():
                    User.objects.filter(pk=user_id).update(is_staff=False)
            return user
        except User.DoesNotExist:
            return None
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Autentizace uživatele."""
        # Použít email místo username
        email = kwargs.get('email') or username
        if email is None:
            return None
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            # Automaticky nastavit is_staff podle role
            if user.role in [User.Role.TEACHER, User.Role.ADMIN] or user.is_superuser:
                # Nastavit v paměti
                user.is_staff = True
                user.is_active = True
                # Uložit do databáze, pokud není nastaveno
                if not User.objects.filter(pk=user.pk, is_staff=True, is_active=True).exists():
                    User.objects.filter(pk=user.pk).update(is_staff=True, is_active=True)
            return user
        return None

