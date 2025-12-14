from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models import Count, Avg, Q
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from .models import Subject, Topic, Feedback
from quizzes.models import Quiz, QuizAttempt
from materials.models import Material


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
        """Přidá okruhy, připomínky a statistiky do kontextu."""
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
        
        # Přidat statistiky pro přihlášené uživatele
        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                # Statistiky pro studenta
                context['student_stats'] = self._get_student_statistics()
            elif self.request.user.is_teacher or self.request.user.is_admin:
                # Statistiky pro učitele
                context['teacher_stats'] = self._get_teacher_statistics()
        
        return context
    
    def _get_student_statistics(self):
        """Vrátí statistiky testů pro studenta v tomto předmětu."""
        # Získat všechny testy v předmětu
        quizzes = Quiz.objects.filter(
            topic__subject=self.object,
            is_published=True
        ).select_related('topic').order_by('topic__order', 'title')
        
        quiz_stats = []
        for quiz in quizzes:
            stats = quiz.get_user_statistics(self.request.user)
            quiz_stats.append({
                'quiz': quiz,
                'topic': quiz.topic,
                **stats
            })
        
        return {
            'quizzes': quiz_stats,
            'total_quizzes': quizzes.count(),
            'attempted_quizzes': sum(1 for q in quiz_stats if q['attempt_count'] > 0)
        }
    
    def _get_teacher_statistics(self):
        """Vrátí statistiky studentů pro učitele v tomto předmětu."""
        from accounts.models import User
        
        # Získat všechny testy v předmětu
        quizzes = Quiz.objects.filter(
            topic__subject=self.object,
            is_published=True
        )
        
        # Získat všechny studenty, kteří mají pokusy v testech tohoto předmětu
        student_ids = QuizAttempt.objects.filter(
            quiz__in=quizzes
        ).values_list('user_id', flat=True).distinct()
        
        students = User.objects.filter(
            id__in=student_ids,
            role=User.Role.STUDENT
        ).order_by('last_name', 'first_name')
        
        student_stats = []
        for student in students:
            # Průměrné skóre přes všechny testy v předmětu
            attempts = QuizAttempt.objects.filter(
                quiz__in=quizzes,
                user=student,
                completed_at__isnull=False,
                score__isnull=False
            )
            
            avg_score = attempts.aggregate(Avg('score'))['score__avg']
            total_attempts = attempts.count()
            
            # Průměrná známka
            avg_grade = None
            if avg_score is not None:
                avg_grade = Quiz.calculate_grade(avg_score)
            
            student_stats.append({
                'student': student,
                'average_score': round(avg_score, 1) if avg_score else None,
                'average_grade': avg_grade,
                'total_attempts': total_attempts,
                'quizzes_attempted': attempts.values('quiz').distinct().count()
            })
        
        return {
            'students': student_stats,
            'total_students': students.count(),
            'total_quizzes': quizzes.count()
        }


class SubjectCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového předmětu (pouze pro učitele/admin)."""
    model = Subject
    template_name = 'subjects/subject_form.html'
    fields = ['name', 'description']
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Automaticky vytvořit slug z názvu."""
        subject = form.save(commit=False)
        subject.slug = slugify(subject.name)
        subject.save()
        messages.success(self.request, f'Předmět "{subject.name}" byl úspěšně vytvořen.')
        return redirect('subjects:subject_detail', subject_slug=subject.slug)


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    """Smazání předmětu (pouze pro učitele/admin)."""
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subjects:subject_list')
    slug_url_kwarg = 'subject_slug'
    slug_field = 'slug'
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Smazat předmět a zobrazit zprávu."""
        subject = self.get_object()
        messages.success(request, f'Předmět "{subject.name}" byl úspěšně smazán.')
        return super().delete(request, *args, **kwargs)


class TopicCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového okruhu (pouze pro učitele/admin)."""
    model = Topic
    template_name = 'subjects/topic_form.html'
    fields = ['name', 'description', 'order']
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Přidat předmět do kontextu."""
        context = super().get_context_data(**kwargs)
        subject_slug = self.kwargs.get('subject_slug')
        context['subject'] = get_object_or_404(Subject, slug=subject_slug)
        return context
    
    def form_valid(self, form):
        """Nastavit předmět a vytvořit slug."""
        subject_slug = self.kwargs.get('subject_slug')
        subject = get_object_or_404(Subject, slug=subject_slug)
        topic = form.save(commit=False)
        topic.subject = subject
        topic.slug = slugify(topic.name)
        topic.save()
        messages.success(self.request, f'Okruh "{topic.name}" byl úspěšně vytvořen.')
        return redirect('subjects:subject_detail', subject_slug=subject.slug)


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    """Smazání okruhu (pouze pro učitele/admin)."""
    model = Topic
    template_name = 'subjects/topic_confirm_delete.html'
    slug_url_kwarg = 'topic_slug'
    slug_field = 'slug'
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """Přesměrovat na detail předmětu po smazání."""
        return reverse_lazy('subjects:subject_detail', kwargs={'subject_slug': self.object.subject.slug})
    
    def delete(self, request, *args, **kwargs):
        """Smazat okruh a zobrazit zprávu."""
        topic = self.get_object()
        messages.success(request, f'Okruh "{topic.name}" byl úspěšně smazán.')
        return super().delete(request, *args, **kwargs)


class QuizCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového testu (pouze pro učitele/admin)."""
    model = Quiz
    template_name = 'quizzes/quiz_form.html'
    fields = ['title', 'description', 'h5p_path', 'time_limit', 'max_attempts', 'passing_score', 'is_published']
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Přidat okruh do kontextu."""
        context = super().get_context_data(**kwargs)
        subject_slug = self.kwargs.get('subject_slug')
        topic_slug = self.kwargs.get('topic_slug')
        context['subject'] = get_object_or_404(Subject, slug=subject_slug)
        context['topic'] = get_object_or_404(Topic, slug=topic_slug, subject__slug=subject_slug)
        return context
    
    def form_valid(self, form):
        """Nastavit okruh a autora."""
        subject_slug = self.kwargs.get('subject_slug')
        topic_slug = self.kwargs.get('topic_slug')
        topic = get_object_or_404(Topic, slug=topic_slug, subject__slug=subject_slug)
        quiz = form.save(commit=False)
        quiz.topic = topic
        quiz.author = self.request.user
        quiz.save()
        messages.success(self.request, f'Test "{quiz.title}" byl úspěšně vytvořen.')
        return redirect('subjects:topic_detail', subject_slug=subject_slug, topic_slug=topic_slug)


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    """Smazání testu (pouze pro učitele/admin)."""
    model = Quiz
    template_name = 'quizzes/quiz_confirm_delete.html'
    pk_url_kwarg = 'pk'
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """Přesměrovat na detail okruhu po smazání."""
        quiz = self.get_object()
        return reverse_lazy('subjects:topic_detail', kwargs={
            'subject_slug': quiz.topic.subject.slug,
            'topic_slug': quiz.topic.slug
        })
    
    def delete(self, request, *args, **kwargs):
        """Smazat test a zobrazit zprávu."""
        quiz = self.get_object()
        messages.success(request, f'Test "{quiz.title}" byl úspěšně smazán.')
        return super().delete(request, *args, **kwargs)


class MaterialCreateView(LoginRequiredMixin, CreateView):
    """Vytvoření nového materiálu (pouze pro učitele/admin)."""
    model = Material
    template_name = 'materials/material_form.html'
    fields = ['title', 'description', 'material_type', 'h5p_path', 'external_url', 'is_published']
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Přidat okruh do kontextu."""
        context = super().get_context_data(**kwargs)
        subject_slug = self.kwargs.get('subject_slug')
        topic_slug = self.kwargs.get('topic_slug')
        context['subject'] = get_object_or_404(Subject, slug=subject_slug)
        context['topic'] = get_object_or_404(Topic, slug=topic_slug, subject__slug=subject_slug)
        return context
    
    def form_valid(self, form):
        """Nastavit okruh a autora."""
        subject_slug = self.kwargs.get('subject_slug')
        topic_slug = self.kwargs.get('topic_slug')
        topic = get_object_or_404(Topic, slug=topic_slug, subject__slug=subject_slug)
        material = form.save(commit=False)
        material.topic = topic
        material.author = self.request.user
        material.save()
        messages.success(self.request, f'Materiál "{material.title}" byl úspěšně vytvořen.')
        return redirect('subjects:topic_detail', subject_slug=subject_slug, topic_slug=topic_slug)


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    """Smazání materiálu (pouze pro učitele/admin)."""
    model = Material
    template_name = 'materials/material_confirm_delete.html'
    pk_url_kwarg = 'pk'
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """Přesměrovat na detail okruhu po smazání."""
        material = self.get_object()
        return reverse_lazy('subjects:topic_detail', kwargs={
            'subject_slug': material.topic.subject.slug,
            'topic_slug': material.topic.slug
        })
    
    def delete(self, request, *args, **kwargs):
        """Smazat materiál a zobrazit zprávu."""
        material = self.get_object()
        messages.success(request, f'Materiál "{material.title}" byl úspěšně smazán.')
        return super().delete(request, *args, **kwargs)


class StudentStatisticsView(LoginRequiredMixin, DetailView):
    """Detail statistik studenta pro učitele."""
    model = Subject
    template_name = 'subjects/student_statistics.html'
    context_object_name = 'subject'
    slug_url_kwarg = 'subject_slug'
    slug_field = 'slug'
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontrolovat, že uživatel je učitel nebo admin."""
        if not (request.user.is_teacher or request.user.is_admin):
            from django.http import Http404
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Přidá statistiky studenta do kontextu."""
        context = super().get_context_data(**kwargs)
        
        # Získat studenta z URL parametru
        from accounts.models import User
        student_id = self.kwargs.get('student_id')
        try:
            student = User.objects.get(id=student_id, role=User.Role.STUDENT)
        except User.DoesNotExist:
            from django.http import Http404
            raise Http404("Student nenalezen")
        
        context['student'] = student
        
        # Získat všechny testy v předmětu
        quizzes = Quiz.objects.filter(
            topic__subject=self.object,
            is_published=True
        ).select_related('topic').order_by('topic__order', 'title')
        
        quiz_stats = []
        for quiz in quizzes:
            stats = quiz.get_user_statistics(student)
            quiz_stats.append({
                'quiz': quiz,
                'topic': quiz.topic,
                **stats
            })
        
        context['quiz_stats'] = quiz_stats
        context['total_quizzes'] = quizzes.count()
        context['attempted_quizzes'] = sum(1 for q in quiz_stats if q['attempt_count'] > 0)
        
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

