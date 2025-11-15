from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Subject, Topic


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
        """Přidá okruhy do kontextu."""
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all()
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
        """Přidá materiály, testy a diskuse do kontextu."""
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['subject'] = topic.subject
        context['materials'] = topic.materials.filter(is_published=True)
        context['quizzes'] = topic.quizzes.filter(is_published=True)
        context['forum_threads'] = topic.forum_threads.all()[:10]  # Posledních 10 vláken
        return context

