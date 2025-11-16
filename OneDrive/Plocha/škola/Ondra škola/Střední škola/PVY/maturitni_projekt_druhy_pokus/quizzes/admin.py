from django.contrib import admin
from .models import Quiz, QuizAttempt


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
            'fields': ('h5p_embed_code',),
            'description': 'Vložte iframe kód pro H5P test'
        }),
    )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'is_passed', 'started_at', 'completed_at']
    list_filter = ['is_passed', 'quiz__topic__subject', 'started_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'quiz__title']
    ordering = ['-started_at']
    readonly_fields = ['started_at']

