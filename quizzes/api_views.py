"""
API views pro H5P integraci - ukládání výsledků z H5P testů.
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, QuizAttempt, H5PUserData
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def h5p_user_data(request, content_id):
    """
    API endpoint pro ukládání a načítání stavu uživatele v H5P obsahu.
    
    GET: Vrací uložený stav uživatele pro daný content_id
    POST: Ukládá nový stav uživatele
    
    Tento endpoint je kompatibilní s h5p-standalone ajax.contentUserDataUrl
    """
    user = request.user
    
    if request.method == 'GET':
        # H5P očekává pole objektů, každý s 'state' a 'subContentId'
        try:
            user_data = H5PUserData.objects.get(user=user, content_id=content_id)
            # H5P očekává formát: [{"state": "...", "subContentId": null}]
            return Response([{
                "state": user_data.data.get('state', ''),
                "subContentId": user_data.data.get('subContentId')
            }])
        except H5PUserData.DoesNotExist:
            # Pokud neexistuje, vrátíme prázdné pole
            return Response([])
    
    elif request.method == 'POST':
        # H5P posílá data ve formátu: [{"state": "...", "subContentId": null}]
        try:
            data = request.data
            if isinstance(data, list) and len(data) > 0:
                state_data = data[0]
                state = state_data.get('state', '')
                sub_content_id = state_data.get('subContentId')
            else:
                # Fallback pro jiný formát
                state = data.get('state', '')
                sub_content_id = data.get('subContentId')
            
            # Uložit nebo aktualizovat
            H5PUserData.objects.update_or_create(
                user=user,
                content_id=content_id,
                defaults={
                    'data': {
                        'state': state,
                        'subContentId': sub_content_id
                    }
                }
            )
            
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def h5p_xapi_event(request):
    """
    API endpoint pro zpracování xAPI událostí z H5P.
    
    H5P posílá xAPI události, které obsahují informace o:
    - Dokončení aktivity
    - Skóre
    - Odpovědích uživatele
    - Času stráveném v aktivitě
    
    Tyto události se ukládají do QuizAttempt.
    """
    try:
        data = request.data
        statement = data.get('statement', {})
        
        # Extrahovat informace z xAPI statement
        verb = statement.get('verb', {})
        verb_id = verb.get('id', '')
        object_data = statement.get('object', {})
        result = statement.get('result', {})
        
        # Získat content_id z object.id (např. "http://h5p.org/interactive-video/123")
        object_id = object_data.get('id', '')
        content_id = object_id.split('/')[-1] if '/' in object_id else None
        
        # Získat skóre
        score_data = result.get('score', {})
        raw_score = score_data.get('raw')
        max_score = score_data.get('max')
        
        # Vypočítat procentuální skóre
        percentage_score = None
        if raw_score is not None and max_score:
            percentage_score = int((raw_score / max_score) * 100)
        
        # Zjistit, jestli je aktivita dokončena
        is_completed = 'completed' in verb_id.lower() or 'passed' in verb_id.lower()
        
        # Pokusit se najít quiz podle content_id nebo jiného identifikátoru
        # Pro teď použijeme content_id jako identifikátor
        # V budoucnu by mohlo být lepší mít explicitní mapování
        quiz_id = request.data.get('quiz_id')  # Pokud je poslán explicitně
        
        if quiz_id:
            try:
                quiz = Quiz.objects.get(id=quiz_id)
                
                # Vytvořit nebo aktualizovat QuizAttempt
                attempt, created = QuizAttempt.objects.get_or_create(
                    quiz=quiz,
                    user=request.user,
                    defaults={
                        'started_at': timezone.now()
                    }
                )
                
                # Aktualizovat skóre a stav
                if percentage_score is not None:
                    attempt.score = percentage_score
                    attempt.is_passed = percentage_score >= quiz.passing_score
                
                if is_completed:
                    attempt.completed_at = timezone.now()
                
                # Uložit celá xAPI data do answers_data
                attempt.answers_data = {
                    'xapi_statement': statement,
                    'content_id': content_id,
                    'verb': verb_id
                }
                
                attempt.save()
                
                return Response({
                    'success': True,
                    'attempt_id': attempt.id,
                    'score': attempt.score,
                    'is_passed': attempt.is_passed
                })
            except Quiz.DoesNotExist:
                return Response({
                    'error': 'Quiz neexistuje'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Pokud není quiz_id, jen logujeme událost
            return Response({
                'success': True,
                'message': 'xAPI událost přijata, ale quiz_id není specifikován'
            })
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

