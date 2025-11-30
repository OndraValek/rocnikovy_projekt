"""
API views pro dynamické načítání úloh (materiálů, testů) z databáze.
"""
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from materials.models import Material
from quizzes.models import Quiz
from subjects.models import Topic, Subject, Feedback


class MaterialsAPIView(LoginRequiredMixin, View):
    """
    API endpoint pro načítání materiálů.
    
    GET parametry:
    - topic_id: ID okruhu (povinné)
    - material_type: typ materiálu (pdf, video, h5p, text, image, link)
    - search: vyhledávání v názvu a popisu
    - page: číslo stránky (default: 1)
    - per_page: počet na stránku (default: 10)
    """
    
    def get(self, request):
        topic_id = request.GET.get('topic_id')
        material_type = request.GET.get('material_type')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        if not topic_id:
            return JsonResponse({
                'error': 'topic_id je povinný'
            }, status=400)
        
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return JsonResponse({
                'error': 'Okruh neexistuje'
            }, status=404)
        
        # Základní queryset
        queryset = Material.objects.filter(
            topic=topic,
            is_published=True
        )
        
        # Filtrování podle typu
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        # Vyhledávání
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Seřazení
        queryset = queryset.order_by('order', 'title')
        
        # Stránkování
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        # Serializace dat
        materials = []
        for material in page_obj:
            materials.append({
                'id': material.id,
                'title': material.title,
                'description': material.description or '',
                'material_type': material.material_type,
                'material_type_display': material.get_material_type_display(),
                'author': material.author.get_full_name() if material.author else '',
                'url': f'/materials/{material.id}/',
                'created_at': material.created_at.strftime('%d.%m.%Y'),
            })
        
        return JsonResponse({
            'success': True,
            'materials': materials,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })


class QuizzesAPIView(LoginRequiredMixin, View):
    """
    API endpoint pro načítání testů.
    
    GET parametry:
    - topic_id: ID okruhu (povinné)
    - search: vyhledávání v názvu a popisu
    - page: číslo stránky (default: 1)
    - per_page: počet na stránku (default: 10)
    """
    
    def get(self, request):
        topic_id = request.GET.get('topic_id')
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        if not topic_id:
            return JsonResponse({
                'error': 'topic_id je povinný'
            }, status=400)
        
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return JsonResponse({
                'error': 'Okruh neexistuje'
            }, status=404)
        
        # Základní queryset
        queryset = Quiz.objects.filter(
            topic=topic,
            is_published=True
        )
        
        # Vyhledávání
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Seřazení
        queryset = queryset.order_by('created_at')
        
        # Stránkování
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        # Získat informace o pokusech uživatele
        user_attempts = {}
        if request.user.is_authenticated:
            attempts = request.user.quiz_attempts.filter(
                quiz__in=queryset
            ).select_related('quiz')
            for attempt in attempts:
                if attempt.quiz_id not in user_attempts:
                    user_attempts[attempt.quiz_id] = {
                        'count': 0,
                        'best_score': None,
                        'is_passed': False
                    }
                user_attempts[attempt.quiz_id]['count'] += 1
                if attempt.score is not None:
                    if (user_attempts[attempt.quiz_id]['best_score'] is None or 
                        attempt.score > user_attempts[attempt.quiz_id]['best_score']):
                        user_attempts[attempt.quiz_id]['best_score'] = attempt.score
                        user_attempts[attempt.quiz_id]['is_passed'] = attempt.is_passed
        
        # Serializace dat
        quizzes = []
        for quiz in page_obj:
            quiz_data = {
                'id': quiz.id,
                'title': quiz.title,
                'description': quiz.description or '',
                'time_limit': quiz.time_limit,
                'max_attempts': quiz.max_attempts,
                'passing_score': quiz.passing_score,
                'url': f'/quiz/{quiz.id}/',
                'created_at': quiz.created_at.strftime('%d.%m.%Y'),
            }
            
            # Přidat informace o pokusech
            if quiz.id in user_attempts:
                quiz_data['user_attempts'] = user_attempts[quiz.id]
                quiz_data['can_attempt'] = user_attempts[quiz.id]['count'] < quiz.max_attempts
            else:
                quiz_data['user_attempts'] = {'count': 0, 'best_score': None, 'is_passed': False}
                quiz_data['can_attempt'] = True
            
            quizzes.append(quiz_data)
        
        return JsonResponse({
            'success': True,
            'quizzes': quizzes,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })


class AllTasksAPIView(LoginRequiredMixin, View):
    """
    API endpoint pro načítání všech úloh (materiály + testy) najednou.
    
    GET parametry:
    - topic_id: ID okruhu (povinné)
    - type: 'materials', 'quizzes', nebo 'all' (default: 'all')
    - search: vyhledávání
    - page: číslo stránky
    - per_page: počet na stránku
    """
    
    def get(self, request):
        topic_id = request.GET.get('topic_id')
        task_type = request.GET.get('type', 'all')  # 'materials', 'quizzes', 'all'
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        if not topic_id:
            return JsonResponse({
                'error': 'topic_id je povinný'
            }, status=400)
        
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return JsonResponse({
                'error': 'Okruh neexistuje'
            }, status=404)
        
        tasks = []
        
        # Načíst materiály
        if task_type in ['materials', 'all']:
            materials = Material.objects.filter(
                topic=topic,
                is_published=True
            )
            
            if search:
                materials = materials.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )
            
            for material in materials.order_by('order', 'title'):
                tasks.append({
                    'id': material.id,
                    'type': 'material',
                    'title': material.title,
                    'description': material.description or '',
                    'material_type': material.get_material_type_display(),
                    'url': f'/materials/{material.id}/',
                    'created_at': material.created_at.strftime('%d.%m.%Y'),
                    'sort_date': material.created_at,  # Pro řazení
                })
        
        # Načíst testy
        if task_type in ['quizzes', 'all']:
            quizzes = Quiz.objects.filter(
                topic=topic,
                is_published=True
            )
            
            if search:
                quizzes = quizzes.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )
            
            # Získat pokusy uživatele
            user_attempts = {}
            if request.user.is_authenticated:
                attempts = request.user.quiz_attempts.filter(
                    quiz__in=quizzes
                ).select_related('quiz')
                for attempt in attempts:
                    if attempt.quiz_id not in user_attempts:
                        user_attempts[attempt.quiz_id] = {
                            'count': 0,
                            'best_score': None
                        }
                    user_attempts[attempt.quiz_id]['count'] += 1
                    if attempt.score is not None:
                        if (user_attempts[attempt.quiz_id]['best_score'] is None or 
                            attempt.score > user_attempts[attempt.quiz_id]['best_score']):
                            user_attempts[attempt.quiz_id]['best_score'] = attempt.score
            
            for quiz in quizzes.order_by('created_at'):
                quiz_data = {
                    'id': quiz.id,
                    'type': 'quiz',
                    'title': quiz.title,
                    'description': quiz.description or '',
                    'time_limit': quiz.time_limit,
                    'max_attempts': quiz.max_attempts,
                    'url': f'/quiz/{quiz.id}/',
                    'created_at': quiz.created_at.strftime('%d.%m.%Y'),
                    'sort_date': quiz.created_at,  # Pro řazení
                }
                
                if quiz.id in user_attempts:
                    quiz_data['user_attempts'] = user_attempts[quiz.id]
                    quiz_data['can_attempt'] = user_attempts[quiz.id]['count'] < quiz.max_attempts
                else:
                    quiz_data['user_attempts'] = {'count': 0, 'best_score': None}
                    quiz_data['can_attempt'] = True
                
                tasks.append(quiz_data)
        
        # Seřadit podle data (nejnovější první)
        tasks.sort(key=lambda x: x['sort_date'], reverse=True)
        
        # Odstranit sort_date z výsledků
        for task in tasks:
            task.pop('sort_date', None)
        
        # Stránkování
        paginator = Paginator(tasks, per_page)
        page_obj = paginator.get_page(page)
        
        return JsonResponse({
            'success': True,
            'tasks': list(page_obj),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })


class FeedbackAPIView(LoginRequiredMixin, View):
    """
    API endpoint pro práci s připomínkami.
    
    GET parametry:
    - content_type: 'subject' nebo 'topic'
    - object_id: ID předmětu nebo okruhu
    - page: číslo stránky (default: 1)
    - per_page: počet na stránku (default: 10)
    
    POST parametry:
    - content_type: 'subject' nebo 'topic'
    - object_id: ID předmětu nebo okruhu
    - text: text připomínky
    """
    
    def get(self, request):
        content_type_name = request.GET.get('content_type')
        object_id = request.GET.get('object_id')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        if not content_type_name or not object_id:
            return JsonResponse({
                'error': 'content_type a object_id jsou povinné'
            }, status=400)
        
        # Získat ContentType
        if content_type_name == 'subject':
            content_type = ContentType.objects.get_for_model(Subject)
        elif content_type_name == 'topic':
            content_type = ContentType.objects.get_for_model(Topic)
        else:
            return JsonResponse({
                'error': 'content_type musí být "subject" nebo "topic"'
            }, status=400)
        
        # Ověřit, že objekt existuje
        try:
            obj = content_type.get_object_for_this_type(id=object_id)
        except:
            return JsonResponse({
                'error': 'Objekt neexistuje'
            }, status=404)
        
        # Načíst připomínky
        queryset = Feedback.objects.filter(
            content_type=content_type,
            object_id=object_id
        ).select_related('author').order_by('-created_at')
        
        # Stránkování
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        # Serializace dat
        feedbacks = []
        for feedback in page_obj:
            feedbacks.append({
                'id': feedback.id,
                'text': feedback.text,
                'author': feedback.author_name,
                'author_role': feedback.author_role,
                'is_edited': feedback.is_edited,
                'created_at': feedback.created_at.strftime('%d.%m.%Y %H:%M'),
                'updated_at': feedback.updated_at.strftime('%d.%m.%Y %H:%M') if feedback.is_edited else None,
                'can_edit': feedback.author == request.user,
            })
        
        return JsonResponse({
            'success': True,
            'feedbacks': feedbacks,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                'error': 'Neplatný JSON'
            }, status=400)
        
        content_type_name = data.get('content_type')
        object_id = data.get('object_id')
        text = data.get('text', '').strip()
        
        if not content_type_name or not object_id:
            return JsonResponse({
                'error': 'content_type a object_id jsou povinné'
            }, status=400)
        
        if not text:
            return JsonResponse({
                'error': 'Text připomínky je povinný'
            }, status=400)
        
        # Získat ContentType
        if content_type_name == 'subject':
            content_type = ContentType.objects.get_for_model(Subject)
        elif content_type_name == 'topic':
            content_type = ContentType.objects.get_for_model(Topic)
        else:
            return JsonResponse({
                'error': 'content_type musí být "subject" nebo "topic"'
            }, status=400)
        
        # Ověřit, že objekt existuje
        try:
            obj = content_type.get_object_for_this_type(id=object_id)
        except:
            return JsonResponse({
                'error': 'Objekt neexistuje'
            }, status=404)
        
        # Vytvořit připomínku
        feedback = Feedback.objects.create(
            content_type=content_type,
            object_id=object_id,
            author=request.user,
            text=text
        )
        
        return JsonResponse({
            'success': True,
            'feedback': {
                'id': feedback.id,
                'text': feedback.text,
                'author': feedback.author_name,
                'author_role': feedback.author_role,
                'is_edited': feedback.is_edited,
                'created_at': feedback.created_at.strftime('%d.%m.%Y %H:%M'),
                'can_edit': True,
            }
        })

