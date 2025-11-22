"""
Wagtail hooks pro správu Quiz modelů v Wagtail adminu.
Pro Wagtail 5.2+ používáme ModelViewSet API.
"""
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import Quiz, QuizAttempt, H5PUserData


class QuizModelViewSet(ModelViewSet):
    """Správa testů v Wagtail adminu."""
    model = Quiz
    menu_label = 'Testy'
    menu_icon = 'form'
    menu_order = 200
    add_to_admin_menu = True
    list_display = ('title', 'topic', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'topic__subject', 'created_at')
    search_fields = ('title', 'description')
    # Zahrnout všechna pole kromě automatických
    exclude_form_fields = ('created_at', 'updated_at')


class QuizAttemptModelViewSet(ModelViewSet):
    """Správa pokusů o testy v Wagtail adminu."""
    model = QuizAttempt
    menu_label = 'Pokusy o testy'
    menu_icon = 'clipboard-list'
    menu_order = 201
    add_to_admin_menu = True
    list_display = ('user', 'quiz', 'score', 'is_passed', 'started_at', 'completed_at')
    list_filter = ('is_passed', 'quiz__topic__subject', 'started_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'quiz__title')
    exclude_form_fields = ()  # Zahrnout všechna pole


class H5PUserDataModelViewSet(ModelViewSet):
    """Správa H5P uživatelských dat v Wagtail adminu."""
    model = H5PUserData
    menu_label = 'H5P uživatelská data'
    menu_icon = 'code'
    menu_order = 202
    add_to_admin_menu = True
    list_display = ('user', 'content_id', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('user__email', 'content_id')
    exclude_form_fields = ('updated_at',)  # updated_at se nastaví automaticky


# Registrace do Wagtail adminu pomocí hooku
@hooks.register("register_admin_viewset")
def register_quiz_viewset():
    return QuizModelViewSet()

@hooks.register("register_admin_viewset")
def register_quiz_attempt_viewset():
    return QuizAttemptModelViewSet()

@hooks.register("register_admin_viewset")
def register_h5p_user_data_viewset():
    return H5PUserDataModelViewSet()

