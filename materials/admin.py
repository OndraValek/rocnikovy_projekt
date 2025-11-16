from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'material_type', 'author', 'is_published', 'created_at']
    list_filter = ['material_type', 'is_published', 'topic__subject', 'created_at']
    search_fields = ['title', 'description', 'content']
    ordering = ['topic', 'order', 'title']
    fieldsets = (
        ('Základní informace', {
            'fields': ('topic', 'title', 'description', 'material_type', 'author', 'order', 'is_published')
        }),
        ('Obsah', {
            'fields': ('document', 'image', 'external_url', 'h5p_embed_code', 'content'),
            'description': 'Vyplňte pole podle typu materiálu'
        }),
    )

