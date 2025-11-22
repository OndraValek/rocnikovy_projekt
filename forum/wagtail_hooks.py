"""
Wagtail hooks pro správu Forum modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import ForumThread, ForumPost


class ForumThreadModelViewSet(ModelViewSet):
    """Správa diskusních vláken v Wagtail adminu."""
    model = ForumThread
    menu_label = 'Diskusní vlákna'
    menu_icon = 'comments'
    menu_order = 300
    add_to_admin_menu = True
    list_display = ('title', 'topic', 'author', 'is_pinned', 'is_locked', 'views', 'created_at')
    list_filter = ('is_pinned', 'is_locked', 'topic__subject', 'created_at')
    search_fields = ('title',)
    exclude_form_fields = ('created_at', 'updated_at', 'views')


class ForumPostModelViewSet(ModelViewSet):
    """Správa příspěvků v Wagtail adminu."""
    model = ForumPost
    menu_label = 'Příspěvky'
    menu_icon = 'comment'
    menu_order = 301
    add_to_admin_menu = True
    list_display = ('thread', 'author', 'is_edited', 'created_at')
    list_filter = ('thread__topic__subject', 'is_edited', 'created_at')
    search_fields = ('content',)
    exclude_form_fields = ('created_at', 'updated_at', 'is_edited')


# Registrace do Wagtail adminu pomocí hooku
@hooks.register("register_admin_viewset")
def register_forum_thread_viewset():
    return ForumThreadModelViewSet()

@hooks.register("register_admin_viewset")
def register_forum_post_viewset():
    return ForumPostModelViewSet()

