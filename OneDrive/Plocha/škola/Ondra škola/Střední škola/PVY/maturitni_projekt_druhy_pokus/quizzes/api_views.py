"""
API views pro H5P integraci - ukládání výsledků z H5P testů.
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Quiz, QuizAttempt
from django.utils import timezone


@method_decorator(csrf_exempt, name='dispatch')
class H5PResultsView(LoginRequiredMixin, View):
    """
    API endpoint pro ukládání výsledků z H5P testů.
    
    Přijímá POST request s JSON daty:
    {
        "quiz_id": 1,
        "attempt_id": 123,  # volitelné
        "score": 85,
        "max_score": 100,
        "time_spent": 300,  # sekundy
        "answers": {...},  # volitelné
        "completed": true
    }
    """
    
    def post(self, request):
        # Zkontrolovat, že uživatel je přihlášen
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Vyžadováno přihlášení'
            }, status=401)
        
        try:
            data = json.loads(request.body)
            
            quiz_id = data.get('quiz_id')
            attempt_id = data.get('attempt_id')
            score = data.get('score')
            max_score = data.get('max_score', 100)
            time_spent = data.get('time_spent')
            answers = data.get('answers')
            completed = data.get('completed', True)
            
            if not quiz_id:
                return JsonResponse({
                    'error': 'quiz_id je povinný'
                }, status=400)
            
            # Získat quiz
            try:
                quiz = Quiz.objects.get(id=quiz_id)
            except Quiz.DoesNotExist:
                return JsonResponse({
                    'error': 'Test neexistuje'
                }, status=404)
            
            # Vypočítat procentuální skóre
            if score is not None and max_score:
                percentage_score = int((score / max_score) * 100)
            else:
                percentage_score = None
            
            # Získat nebo vytvořit attempt
            if attempt_id:
                try:
                    attempt = QuizAttempt.objects.get(
                        id=attempt_id,
                        quiz=quiz,
                        user=request.user
                    )
                except QuizAttempt.DoesNotExist:
                    attempt = QuizAttempt.objects.create(
                        quiz=quiz,
                        user=request.user
                    )
            else:
                # Vytvořit nový attempt
                attempt = QuizAttempt.objects.create(
                    quiz=quiz,
                    user=request.user
                )
            
            # Aktualizovat attempt
            if percentage_score is not None:
                attempt.score = percentage_score
                attempt.is_passed = percentage_score >= quiz.passing_score
            
            if completed:
                attempt.completed_at = timezone.now()
            
            if answers:
                attempt.answers_data = answers
            
            attempt.save()
            
            return JsonResponse({
                'success': True,
                'attempt_id': attempt.id,
                'score': attempt.score,
                'is_passed': attempt.is_passed,
                'message': 'Výsledky byly úspěšně uloženy'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Neplatný JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)

