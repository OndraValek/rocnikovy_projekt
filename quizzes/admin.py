from django.contrib import admin
from .models import Quiz, QuizAttempt, H5PUserData


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'topic__subject', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['topic', 'created_at']
    fieldsets = (
        ('Základní informace', {
            'fields': ('topic', 'title', 'description', 'author', 'is_published')
        }),
        ('Nastavení testu', {
            'fields': ('time_limit', 'max_attempts', 'passing_score')
        }),
        ('H5P obsah', {
            'fields': ('h5p_path', 'h5p_embed_code',),
            'description': 'Pro h5p-standalone použijte h5p_path (cesta k rozbalenému H5P obsahu). Pro starší způsob použijte h5p_embed_code.'
        }),
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'is_passed', 'started_at', 'completed_at']
    list_filter = ['is_passed', 'quiz__topic__subject', 'started_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'quiz__title']
    ordering = ['-started_at']
    readonly_fields = ['started_at']


@admin.register(H5PUserData)
class H5PUserDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_id', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__email', 'content_id']
    ordering = ['-updated_at']
    readonly_fields = ['updated_at']

