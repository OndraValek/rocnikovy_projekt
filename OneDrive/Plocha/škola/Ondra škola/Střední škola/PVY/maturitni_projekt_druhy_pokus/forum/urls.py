from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('forum/topic/<int:topic_id>/thread/create/', views.create_thread, name='create_thread'),
    path('forum/thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('forum/thread/<int:thread_id>/post/', views.create_post, name='create_post'),
    path('forum/post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('forum/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]

