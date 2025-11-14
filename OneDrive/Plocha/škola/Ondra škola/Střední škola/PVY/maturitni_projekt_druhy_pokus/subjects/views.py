from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Topic


def subject_list(request):
    """Seznam všech předmětů."""
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
    }
    return render(request, 'subjects/subject_list.html', context)


def subject_detail(request, subject_slug):
    """Detail předmětu s okruhy."""
    subject = get_object_or_404(Subject, slug=subject_slug)
    topics = subject.topics.all()
    context = {
        'subject': subject,
        'topics': topics,
    }
    return render(request, 'subjects/subject_detail.html', context)


@login_required
def topic_detail(request, subject_slug, topic_slug):
    """Detail okruhu s materiály, testy a fórem."""
    subject = get_object_or_404(Subject, slug=subject_slug)
    topic = get_object_or_404(Topic, subject=subject, slug=topic_slug)
    
    # Získat materiály, testy a diskuse
    materials = topic.materials.all()
    quizzes = topic.quizzes.filter(is_published=True)
    forum_threads = topic.forum_threads.all()[:10]  # Posledních 10 vláken
    
    context = {
        'subject': subject,
        'topic': topic,
        'materials': materials,
        'quizzes': quizzes,
        'forum_threads': forum_threads,
    }
    return render(request, 'subjects/topic_detail.html', context)

