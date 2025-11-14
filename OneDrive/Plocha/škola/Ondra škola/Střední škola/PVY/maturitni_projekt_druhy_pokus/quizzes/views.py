from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Quiz, QuizAttempt


@login_required
def quiz_detail(request, quiz_id):
    """Detail testu."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Zkontrolovat, kolik pokusů uživatel má
    user_attempts = quiz.attempts.filter(user=request.user).count()
    can_attempt = user_attempts < quiz.max_attempts
    
    # Poslední pokus
    last_attempt = quiz.attempts.filter(user=request.user).order_by('-started_at').first()
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts,
        'can_attempt': can_attempt,
        'last_attempt': last_attempt,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def quiz_attempt(request, quiz_id):
    """Spuštění testu."""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Zkontrolovat počet pokusů
    user_attempts = quiz.attempts.filter(user=request.user).count()
    if user_attempts >= quiz.max_attempts:
        messages.error(request, 'Dosáhl jsi maximálního počtu pokusů pro tento test.')
        return redirect('quizzes:quiz_detail', quiz_id=quiz.id)
    
    # Vytvořit nový pokus
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        user=request.user
    )
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
    }
    return render(request, 'quizzes/quiz_attempt.html', context)


@login_required
def quiz_result(request, attempt_id):
    """Výsledek testu."""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    context = {
        'attempt': attempt,
        'quiz': attempt.quiz,
    }
    return render(request, 'quizzes/quiz_result.html', context)

