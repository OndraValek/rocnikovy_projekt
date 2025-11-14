from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/attempt/', views.quiz_attempt, name='quiz_attempt'),
    path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
]

