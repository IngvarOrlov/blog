import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

from .models import Post, User
from .forms import PostForm, CommentForm
from .slug import make_unique_slug


# Create your views here.

def posts(request):
    post_list = Post.objects.select_related("author").all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'main/post_list.html', {"object_list": posts})


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


def show_post(request, slug):
    try:
        post = Post.objects.select_related("author").get(slug=slug)
        comments = post.comments.filter(active=True)
        form = CommentForm()
        return render(request,
                      'main/post_detail.html',
                      {'post': post, 'form': form, 'comments': comments})
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Post not found</h2>')


@login_required
def update_post(request, slug):
    # post = get_object_or_404(Post, slug=slug)
    try:
        post = Post.objects.get(slug=slug)
        # GET
        if post.author_id != request.user.id:
            return redirect('index')
        if request.method == 'GET':
            form = PostForm(model_to_dict(post))
            return render(request, 'main/post_update.html', {'form': form})
        # POST
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.save()
        messages.success(request, 'Post succesfully edited!')
        return render(request, 'main/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Post not found</h2>')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostListView(ListView):
    model = Post


@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post,
                             slug=slug)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        commentator = User.objects.get(id=request.user.id)
        comment.name = commentator
        comment.save()
        messages.success(request, 'Комментарий создан успешно')
    else:
        messages.error(request, 'ой, ошибка!')
    # return render(request, 'main/comment.html',
    #               {'post': post,
    #                'form': form,
    #                'comment': comment})
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'main/post_detail.html',
                  {'post': post, 'form': form, 'comments': comments})
