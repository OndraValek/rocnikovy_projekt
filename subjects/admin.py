from django.contrib import admin
from .models import Subject, Topic, Feedback


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['subject', 'order', 'name']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'content_type', 'object_id', 'created_at', 'is_edited']
    list_filter = ['content_type', 'is_edited', 'created_at']
    search_fields = ['text', 'author__email', 'author__first_name', 'author__last_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Obsah', {
            'fields': ('content_type', 'object_id', 'text')
        }),
        ('Autor', {
            'fields': ('author',)
        }),
        ('Metadata', {
            'fields': ('is_edited', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

