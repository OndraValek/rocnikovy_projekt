from django.urls import path
from . import views
from . import api_views

app_name = 'quizzes'

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/attempt/', views.QuizAttemptView.as_view(), name='quiz_attempt'),
    path('attempt/<int:attempt_id>/', views.QuizAttemptDetailView.as_view(), name='quiz_attempt_detail'),
    # API endpoint pro H5P výsledky
    path('api/h5p/results/', api_views.H5PResultsView.as_view(), name='h5p_results'),
]

