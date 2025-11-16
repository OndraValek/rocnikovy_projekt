from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from .models import Quiz, QuizAttempt


class QuizDetailView(LoginRequiredMixin, DetailView):
    """Detail testu."""
    model = Quiz
    template_name = 'quizzes/quiz_detail.html'
    context_object_name = 'quiz'
    pk_url_kwarg = 'quiz_id'
    
    def get_queryset(self):
        """Filtruje pouze publikované testy."""
        return Quiz.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        """Přidá informace o pokusech uživatele."""
        context = super().get_context_data(**kwargs)
        quiz = self.object
        
        # Zkontrolovat, kolik pokusů uživatel má
        user_attempts = quiz.attempts.filter(user=self.request.user).count()
        can_attempt = user_attempts < quiz.max_attempts
        
        # Poslední pokus
        last_attempt = quiz.attempts.filter(user=self.request.user).order_by('-started_at').first()
        
        context['user_attempts'] = user_attempts
        context['can_attempt'] = can_attempt
        context['last_attempt'] = last_attempt
        return context


class QuizAttemptView(LoginRequiredMixin, CreateView):
    """Spuštění testu."""
    model = QuizAttempt
    template_name = 'quizzes/quiz_attempt.html'
    fields = []  # Vytvoříme pokus bez polí
    
    def dispatch(self, request, *args, **kwargs):
        """Zkontroluje počet pokusů před zobrazením."""
        self.quiz = get_object_or_404(Quiz, id=kwargs['quiz_id'], is_published=True)
        user_attempts = self.quiz.attempts.filter(user=request.user).count()
        
        if user_attempts >= self.quiz.max_attempts:
            messages.error(request, 'Dosáhl jsi maximálního počtu pokusů pro tento test.')
            return redirect('quizzes:quiz_detail', quiz_id=self.quiz.id)
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Nastaví quiz a uživatele při vytváření pokusu."""
        form.instance.quiz = self.quiz
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Přidá quiz a attempt do kontextu."""
        context = super().get_context_data(**kwargs)
        context['quiz'] = self.quiz
        # Pokud už existuje attempt (po vytvoření), přidat ho do kontextu
        if self.object:
            context['attempt'] = self.object
        return context
    
    def get_success_url(self):
        """Přesměruje na stránku s pokusem."""
        return reverse_lazy('quizzes:quiz_attempt_detail', kwargs={'attempt_id': self.object.id})


class QuizAttemptDetailView(LoginRequiredMixin, DetailView):
    """Výsledek testu."""
    model = QuizAttempt
    template_name = 'quizzes/quiz_result.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
    
    def get_queryset(self):
        """Filtruje pouze pokusy aktuálního uživatele."""
        return QuizAttempt.objects.filter(user=self.request.user)

