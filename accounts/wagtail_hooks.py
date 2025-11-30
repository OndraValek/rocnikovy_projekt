"""
Wagtail hooks pro správu User a UserProfile modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import User, UserProfile, StudentClass


class UserModelViewSet(ModelViewSet):
    """Správa uživatelů v Wagtail adminu."""
    model = User
    menu_label = 'Uživatelé'
    menu_icon = 'user'
    menu_order = 50
    add_to_admin_menu = True
    list_display = ('email', 'first_name', 'last_name', 'role', 'class_name', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    # Vyloučit citlivá pole a automaticky nastavovaná pole
    exclude_form_fields = (
        'password',  # Heslo se nastavuje jinak
        'last_login',
        'date_joined',
        'created_at',
        'updated_at',
        'user_permissions',
        'groups',
    )


class UserProfileModelViewSet(ModelViewSet):
    """Správa uživatelských profilů v Wagtail adminu."""
    model = UserProfile
    menu_label = 'Uživatelské profily'
    menu_icon = 'user'
    menu_order = 51
    add_to_admin_menu = True
    list_display = ('user', 'bio')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bio')
    exclude_form_fields = ()  # Zahrnout všechna pole


class StudentClassModelViewSet(ModelViewSet):
    """Správa tříd/skupin studentů v Wagtail adminu."""
    model = StudentClass
    menu_label = 'Třídy'
    menu_icon = 'group'
    menu_order = 52
    add_to_admin_menu = True
    list_display = ('name', 'teacher', 'get_student_count', 'school_year', 'created_at')
    list_filter = ('school_year', 'created_at', 'teacher')
    search_fields = ('name', 'description', 'teacher__email', 'teacher__first_name', 'teacher__last_name')
    exclude_form_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Učitel vidí jen své třídy, admin vidí všechny."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin):
            return qs
        if hasattr(request.user, 'is_teacher') and request.user.is_teacher:
            return qs.filter(teacher=request.user)
        return qs.none()


# Registrace do Wagtail adminu pomocí hooku
@hooks.register("register_admin_viewset")
def register_user_viewset():
    return UserModelViewSet()


@hooks.register("register_admin_viewset")
def register_user_profile_viewset():
    return UserProfileModelViewSet()


@hooks.register("register_admin_viewset")
def register_student_class_viewset():
    return StudentClassModelViewSet()

