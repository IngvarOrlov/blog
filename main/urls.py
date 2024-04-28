from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

from main import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/back/', views.back_to_posts, name='back_to_posts'),
    # path('posts/', views.PostListView.as_view(), name='posts'),

    path('', views.index, name='index'),
    path('posts/add_new/', views.addpost, name='addpost'),
    path('posts/<slug:slug>', views.show_post, name='showpost'),
    path('posts/<slug:slug>/edit', views.update_post, name='updatepost'),
    path('posts/<slug:slug>/', views.post_comment, name='post_comment'),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='PostDetailView'),

]
