import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages

from .models import Post, User
from .forms import PostForm
from .slug import make_unique_slug


# Create your views here.

def posts(request):
    posts = Post.objects.select_related("user").all()
    # print(posts.query)
    return render(request, 'blog/posts.html', {"posts": posts})


def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'user_list': users})


@login_required
def addpost(request):
    # GET
    if request.method == 'GET':
        newform = PostForm()
        return render(request, 'main/addpost.html', {'form': newform})

    # POST
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(id=user_id)
    slug = make_unique_slug(request.POST.get('title'))

    Post.objects.create(
        title=request.POST.get('title'),
        body=request.POST.get('body'),
        author=user,
        slug=slug
    )
    messages.success(request, "Post successfully added")
    return redirect('posts')


def show_post(request, id):
    try:
        post = Post.objects.select_related("user").get(id=id)
        return render(request, 'main/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Post not found</h2>')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostListView(ListView):
    model = Post
