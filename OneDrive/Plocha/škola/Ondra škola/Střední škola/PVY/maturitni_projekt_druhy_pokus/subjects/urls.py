from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('<slug:subject_slug>/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
]

