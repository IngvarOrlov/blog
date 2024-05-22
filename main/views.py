import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from .models import Post, User, Category, Comment
from .forms import PostForm, CommentForm, SearchForm
from .slug import make_unique_slug


# Create your views here.

def posts(request, tag_slug=None):
    post_list = Post.objects.select_related("author").filter(status='PB')
    tag = None
    title = "Blog"
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        title = "Записи с тэгом " + tag.__str__()

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    # if redirect: pull page from cookie
    if request.COOKIES.get('redirect'):
        page_number = request.COOKIES.get('back_page')
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    html = render(request, 'main/post_list.html', {"object_list": posts, 'tag': tag, 'title': title})
    html.set_cookie('back_page', page_number)
    if request.COOKIES.get('redirect'):
        html.delete_cookie('redirect')
    return html


def back_to_posts(request):
    html = redirect('posts')
    html.set_cookie('redirect', 'True')
    return html


def index(request):
    categories = Category.objects.all()
    return render(request,
                  'index.html',
                  {'categories': categories})


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
    tag_list = str(request.POST.get('tags')).split(',')
    # print(tag_list)
    cat = Category.objects.get(id=request.POST.get('category'))
    post = Post.objects.create(
        title=request.POST.get('title'),
        body=request.POST.get('body'),
        author=user,
        slug=slug,
        category=cat,
    )
    for tag in tag_list:
        post.tags.add(tag.strip())

    messages.success(request, "Пост успешно добавлен")
    return redirect('posts')


def show_post(request, slug):
    try:
        post = Post.objects.select_related("author").get(slug=slug)
        comments = post.comments.filter(active=True)
        form = CommentForm()
        # Список схожих постов
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='PB').exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('slug')).order_by('-same_tags', '-publish')[:4]
        html = render(request,
                      'main/post_detail.html',
                      {'post': post,
                       'form': form,
                       'comments': comments,
                       'similar_posts': similar_posts})
        return html
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
            dict_model = model_to_dict(post)
            tags = [tag.name for tag in post.tags.all()]
            tags = ', '.join(tags)
            dict_model['tags'] = tags
            form = PostForm(dict_model)
            return render(request, 'main/post_update.html', {'form': form, 'post': post, 'title': 'Update'})
        # POST
        # post.tags
        tag_list = str(request.POST.get('tags')).split(',')
        for tag in post.tags.all():
            post.tags.remove(tag)
        for tag in tag_list:
            post.tags.add(tag.strip())
        post.category = Category.objects.get(id=request.POST.get('category'))
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.save()
        messages.success(request, 'Пост успешно изменен')
        return render(request, 'main/post_detail.html', {'post': post})
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Post not found</h2>')


@login_required
def delete_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        if post.author_id != request.user.id:
            return redirect('index')
        post.delete()
        messages.success(request, 'Пост успешно удален')
        return redirect('posts')
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
    comment = Comment()
    comment.body = request.POST.get('body', '')
    comment.post = post
    commentator = User.objects.get(id=request.user.id)
    comment.name = commentator
    if request.POST.get('parent'):
        parent = Comment.objects.get(id=int(request.POST.get('parent')))
        comment.parent = parent
    messages.success(request, 'Комментарий создан успешно')
    comment.save()

    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'main/post_detail.html',
                  {'post': post, 'form': form, 'comments': comments})

@login_required
def post_comment_delete(request, com_id):
    try:
        comment = Comment.objects.get(id=com_id)
    except Comment.DoesNotExist:
        return HttpResponseNotFound('<h2>Comment not found</h2>')
    if comment.name != request.user:
        return redirect('index')
    post = comment.post
    comment.delete()
    messages.success(request, 'Комментарий удален')
    return redirect('showpost', slug=post.slug)

def posts_search(request):
    form = SearchForm()
    query = None
    results = []

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Post.objects.filter(status='PB').annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
            if not results:
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                results = Post.objects.filter(status='PB').annotate(
                    rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')

    return render(request,
                  'main/search.html',
                  {'form': form,
                   'query': query,
                   'object_list': results})


class PostFromCategory(ListView):
    template_name = 'main/post_list_category.html'
    context_object_name = 'posts'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Post.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи из категории: {self.category.title}'
        context['category'] = self.category
        return context
