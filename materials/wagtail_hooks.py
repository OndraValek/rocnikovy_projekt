"""
Wagtail hooks pro správu Material modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import Material


class MaterialModelViewSet(ModelViewSet):
    """Správa materiálů v Wagtail adminu."""
    model = Material
    menu_label = 'Materiály'
    menu_icon = 'doc-full'
    menu_order = 150
    add_to_admin_menu = True
    list_display = ('title', 'topic', 'material_type', 'author', 'created_at')
    list_filter = ('material_type', 'topic__subject', 'created_at')
    search_fields = ('title', 'description')
    exclude_form_fields = ('created_at', 'updated_at')


# Registrace do Wagtail adminu pomocí hooku
@hooks.register("register_admin_viewset")
def register_material_viewset():
    return MaterialModelViewSet()

