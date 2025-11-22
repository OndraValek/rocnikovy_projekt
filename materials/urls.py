from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('materials/<int:material_id>/', views.MaterialDetailView.as_view(), name='material_detail'),
]

