from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('material/<int:material_id>/', views.material_detail, name='material_detail'),
]

