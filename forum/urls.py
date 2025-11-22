from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('forum/topic/<int:topic_id>/thread/create/', views.ThreadCreateView.as_view(), name='create_thread'),
    path('forum/thread/<int:thread_id>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('forum/thread/<int:thread_id>/post/', views.PostCreateView.as_view(), name='create_post'),
    path('forum/post/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('forum/post/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]

