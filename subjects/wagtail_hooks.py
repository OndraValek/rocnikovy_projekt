"""
Wagtail hooks pro správu Subject a Topic modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import Subject, Topic, Feedback


class SubjectModelViewSet(ModelViewSet):
    """Správa předmětů v Wagtail adminu."""
    model = Subject
    menu_label = 'Předměty'
    menu_icon = 'folder'
    menu_order = 100
    add_to_admin_menu = True
    list_display = ('name', 'slug', 'get_classes_display', 'created_at')
    search_fields = ('name', 'description')
    exclude_form_fields = ('created_at', 'updated_at')


class TopicModelViewSet(ModelViewSet):
    """Správa okruhů v Wagtail adminu."""
    model = Topic
    menu_label = 'Okruhy'
    menu_icon = 'folder-open'
    menu_order = 101
    add_to_admin_menu = True
    list_display = ('name', 'subject', 'slug', 'created_at')
    list_filter = ('subject',)
    search_fields = ('name', 'description')
    exclude_form_fields = ('created_at', 'updated_at')


class FeedbackModelViewSet(ModelViewSet):
    """Správa připomínek v Wagtail adminu."""
    model = Feedback
    menu_label = 'Připomínky'
    menu_icon = 'comment'
    menu_order = 102
    add_to_admin_menu = True
    list_display = ('__str__', 'author', 'content_type', 'object_id', 'created_at', 'is_edited')
    list_filter = ('content_type', 'is_edited', 'created_at')
    search_fields = ('text', 'author__email', 'author__first_name', 'author__last_name')
    exclude_form_fields = ('created_at', 'updated_at')


# Registrace do Wagtail adminu pomocí hooku
@hooks.register("register_admin_viewset")
def register_subject_viewset():
    return SubjectModelViewSet()

@hooks.register("register_admin_viewset")
def register_topic_viewset():
    return TopicModelViewSet()


@hooks.register("register_admin_viewset")
def register_feedback_viewset():
    return FeedbackModelViewSet()

