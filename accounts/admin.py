from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, StudentClass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'class_name']
    list_filter = ['role']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['last_name', 'first_name']
    
    # Zobrazit jen požadovaná pole: role, email, křestní jméno, příjmení, třída
    # Odstranit všechna ostatní pole (Superuživatel, Uživatelské jméno, Administrační přístup, Aktivní)
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'role', 'class_name')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'role', 'class_name', 'password1', 'password2')
        }),
    )
    
    # Vyloučit všechna pole, která nechceme zobrazovat
    exclude = ('username', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login', 
               'user_permissions', 'groups', 'created_at', 'updated_at')
    
    def has_change_permission(self, request, obj=None):
        """Učitel může upravovat jen studenty, admin může upravovat všechny."""
        if request.user.is_superuser or request.user.is_admin:
            return True
        if request.user.is_teacher:
            # Učitel může upravovat jen studenty
            if obj is None:
                return True  # Při zobrazení seznamu
            return obj.is_student
        return False
    
    def get_readonly_fields(self, request, obj=None):
        """Omezit editovatelná pole podle role."""
        readonly = list(super().get_readonly_fields(request, obj))
        
        if request.user.is_teacher and not request.user.is_admin:
            # Učitel (ne admin) může upravovat jen roli studentů
            if obj and not obj.is_student:
                readonly.append('role')  # Učitel nemůže měnit roli učitelů/adminů
        elif not (request.user.is_superuser or request.user.is_admin):
            # Student nemůže nic upravovat
            readonly.extend(['role', 'class_name'])
        
        return readonly
    
    def get_form(self, request, obj=None, **kwargs):
        """Upravit formulář podle role uživatele."""
        form = super().get_form(request, obj, **kwargs)
        
        if request.user.is_teacher and not request.user.is_admin:
            # Učitel může nastavit jen roli studenta
            if obj is None or obj.is_student:
                # Omezit výběr rolí jen na studenta
                from django.utils.translation import gettext_lazy as _
                form.base_fields['role'].choices = [
                    (User.Role.STUDENT, _('Student'))
                ]
        
        return form


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'get_student_count', 'school_year', 'created_at']
    list_filter = ['school_year', 'created_at', 'teacher']
    search_fields = ['name', 'description', 'teacher__email', 'teacher__first_name', 'teacher__last_name']
    filter_horizontal = ['students']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Základní informace', {
            'fields': ('name', 'teacher', 'description', 'school_year')
        }),
        ('Studenti', {
            'fields': ('students',),
            'description': 'Vyberte studenty, kteří patří do této třídy'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Učitel vidí jen své třídy, admin vidí všechny."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        if request.user.is_teacher:
            return qs.filter(teacher=request.user)
        return qs.none()
    
    def save_model(self, request, obj, form, change):
        """Automaticky nastavit učitele, pokud není nastaven a uživatel je učitel."""
        if not change and request.user.is_teacher and not obj.teacher_id:
            obj.teacher = request.user
        super().save_model(request, obj, form, change)

