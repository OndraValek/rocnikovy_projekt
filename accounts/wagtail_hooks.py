"""
Wagtail hooks pro správu User a UserProfile modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import User, UserProfile, StudentClass


@hooks.register('construct_wagtail_userbar')
def add_custom_userbar_items(request, items):
    """Přidat vlastní položky do userbar."""
    pass


@hooks.register('before_serve_page')
def check_user_permissions(page, request, serve_args, serve_kwargs):
    """Kontrola oprávnění před zobrazením stránky."""
    pass


class UserModelViewSet(ModelViewSet):
    """Správa uživatelů v Wagtail adminu."""
    model = User
    menu_label = 'Uživatelé'
    menu_icon = 'user'
    menu_order = 50
    add_to_admin_menu = True
    list_display = ('email', 'first_name', 'last_name', 'role', 'class_name')
    list_filter = ('role',)
    search_fields = ('email', 'first_name', 'last_name')
    # Vyloučit všechna pole kromě požadovaných: role, email, křestní jméno, příjmení, třída
    exclude_form_fields = (
        'password',  # Heslo se nastavuje jinak
        'username',  # Nepoužíváme username
        'last_login',
        'date_joined',
        'created_at',
        'updated_at',
        'user_permissions',
        'groups',
        'is_superuser',  # Odstranit superuser
        'is_staff',  # Odstranit staff status (nastavuje se automaticky)
        'is_active',  # Odstranit active status
    )
    
    def get_queryset(self, request):
        """Omezit zobrazení podle role."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin):
            return qs
        if hasattr(request.user, 'is_teacher') and request.user.is_teacher:
            # Učitel vidí všechny uživatele (aby mohl upravovat studenty)
            return qs
        return qs.none()
    
    def get_form(self, request, obj=None, **kwargs):
        """Upravit formulář podle role uživatele."""
        form = super().get_form(request, obj, **kwargs)
        
        if hasattr(request.user, 'is_teacher') and request.user.is_teacher and not (hasattr(request.user, 'is_admin') and request.user.is_admin):
            # Učitel (ne admin) může upravovat jen roli studentů
            if obj is None or obj.is_student:
                # Omezit výběr rolí jen na studenta
                from django.utils.translation import gettext_lazy as _
                form.base_fields['role'].choices = [
                    (User.Role.STUDENT, _('Student'))
                ]
            elif obj:
                # Učitel nemůže upravovat roli učitelů/adminů
                form.base_fields['role'].widget.attrs['readonly'] = True
                form.base_fields['role'].widget.attrs['disabled'] = True
        
        return form
    
    def has_add_permission(self, request):
        """Kdo může přidávat uživatele."""
        return request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin)
    
    def has_edit_permission(self, request, obj):
        """Kdo může upravovat uživatele."""
        if request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin):
            return True
        if hasattr(request.user, 'is_teacher') and request.user.is_teacher:
            # Učitel může upravovat jen studenty
            return obj.is_student
        return False
    
    def has_delete_permission(self, request, obj):
        """Kdo může mazat uživatele."""
        return request.user.is_superuser or (hasattr(request.user, 'is_admin') and request.user.is_admin)


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

