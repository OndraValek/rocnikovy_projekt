from django.contrib import admin
from .models import ForumThread, ForumPost


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'author', 'is_pinned', 'is_locked', 'created_at', 'views']
    list_filter = ['is_pinned', 'is_locked', 'topic__subject', 'created_at']
    search_fields = ['title', 'author__email', 'author__first_name', 'author__last_name']
    ordering = ['-is_pinned', '-updated_at']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'is_edited']
    list_filter = ['created_at', 'is_edited', 'thread__topic__subject']
    search_fields = ['content', 'author__email', 'thread__title']
    ordering = ['-created_at']

