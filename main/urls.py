from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import posts, index, addpost, show_post, PostDetailView, PostListView

urlpatterns = [
    # path('posts/', posts, name='posts'),
    path('posts/', PostListView.as_view(), name='posts'),

    path('', index, name='index'),
    path('posts/add_new/', addpost, name='addpost'),
    # path('posts/<int:id>', show_post, name='showpost'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='PostDetailView'),

]
