from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

from main import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('posts/<str:tag_slug>', views.posts, name='posts_by_tag'),
    path('posts/search/', views.posts_search, name='posts_search'),
    path('posts/back/', views.back_to_posts, name='back_to_posts'),
    # path('posts/', views.PostListView.as_view(), name='posts'),
    path('category/<slug:slug>/', views.PostFromCategory.as_view(), name="post_by_category"),

    path('', views.index, name='index'),
    path('posts/add_new/', views.addpost, name='addpost'),
    path('post/<slug:slug>', views.show_post, name='showpost'),
    path('post/<slug:slug>/edit', views.update_post, name='updatepost'),
    path('post/<slug:slug>/delete', views.delete_post, name='deletepost'),
    path('post/<slug:slug>/', views.post_comment, name='post_comment'),
    path('post/del_com/<int:com_id>', views.post_comment_delete, name='post_comment_delete'),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='PostDetailView'),

]
