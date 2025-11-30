from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, StudentClass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'class_name', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['last_name', 'first_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Další informace', {
            'fields': ('role', 'class_name')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Další informace', {
            'fields': ('role', 'class_name', 'email')
        }),
    )


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

