from django.urls import path
from . import views
from . import api_views

app_name = 'subjects'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('create/', views.SubjectCreateView.as_view(), name='subject_create'),
    # URL pro mazání testů a materiálů (musí být před slug patterns, aby se neshodovaly)
    path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
    path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
    path('<slug:subject_slug>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('<slug:subject_slug>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('<slug:subject_slug>/topic/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('<slug:subject_slug>/<slug:topic_slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('<slug:subject_slug>/<slug:topic_slug>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('<slug:subject_slug>/<slug:topic_slug>/quiz/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('<slug:subject_slug>/<slug:topic_slug>/material/create/', views.MaterialCreateView.as_view(), name='material_create'),
    path('<slug:subject_slug>/student/<int:student_id>/', views.StudentStatisticsView.as_view(), name='student_statistics'),
]

# API endpointy - musí být na rootu, ne v subjects namespace
api_urlpatterns = [
    path('materials/', api_views.MaterialsAPIView.as_view(), name='api_materials'),
    path('quizzes/', api_views.QuizzesAPIView.as_view(), name='api_quizzes'),
    path('tasks/', api_views.AllTasksAPIView.as_view(), name='api_tasks'),
    path('feedback/', api_views.FeedbackAPIView.as_view(), name='api_feedback'),
]

