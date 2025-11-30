from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Subject, Topic, Feedback


class SubjectListView(ListView):
    """Seznam všech předmětů."""
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'
    ordering = ['name']
    
    def get_queryset(self):
        """Vrátí předměty s počtem okruhů."""
        return Subject.objects.annotate(
            topics_count=Count('topics')
        ).all()


class SubjectDetailView(DetailView):
    """Detail předmětu s okruhy."""
    model = Subject
    template_name = 'subjects/subject_detail.html'
    context_object_name = 'subject'
    slug_url_kwarg = 'subject_slug'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        """Přidá okruhy a připomínky do kontextu."""
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
        # Přidat připomínky pro předmět
        content_type = ContentType.objects.get_for_model(Subject)
        context['feedbacks'] = Feedback.objects.filter(
            content_type=content_type,
            object_id=self.object.id
        ).select_related('author').order_by('-created_at')[:10]
        context['feedback_count'] = Feedback.objects.filter(
            content_type=content_type,
            object_id=self.object.id
        ).count()
        return context


class TopicDetailView(LoginRequiredMixin, DetailView):
    """Detail okruhu s materiály, testy a fórem."""
    model = Topic
    template_name = 'subjects/topic_detail.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'
    slug_field = 'slug'
    
    def get_queryset(self):
        """Filtruje okruh podle předmětu."""
        subject_slug = self.kwargs.get('subject_slug')
        return Topic.objects.filter(subject__slug=subject_slug)
    
    def get_context_data(self, **kwargs):
        """Přidá materiály, testy, diskuse a připomínky do kontextu."""
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['subject'] = topic.subject
        context['materials'] = topic.materials.filter(is_published=True)
        context['quizzes'] = topic.quizzes.filter(is_published=True)
        context['forum_threads'] = topic.forum_threads.all()[:10]  # Posledních 10 vláken
        # Přidat připomínky pro okruh
        content_type = ContentType.objects.get_for_model(Topic)
        context['feedbacks'] = Feedback.objects.filter(
            content_type=content_type,
            object_id=topic.id
        ).select_related('author').order_by('-created_at')[:10]
        context['feedback_count'] = Feedback.objects.filter(
            content_type=content_type,
            object_id=topic.id
        ).count()
        return context

