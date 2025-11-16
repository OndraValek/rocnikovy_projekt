from django.urls import path
from . import views
from . import api_views

app_name = 'subjects'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('<slug:subject_slug>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('<slug:subject_slug>/<slug:topic_slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
]

# API endpointy - musí být na rootu, ne v subjects namespace
api_urlpatterns = [
    path('materials/', api_views.MaterialsAPIView.as_view(), name='api_materials'),
    path('quizzes/', api_views.QuizzesAPIView.as_view(), name='api_quizzes'),
    path('tasks/', api_views.AllTasksAPIView.as_view(), name='api_tasks'),
]

