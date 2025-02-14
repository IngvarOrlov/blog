from django import template
from ..models import Post, Comment
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(status='PB').count()


@register.simple_tag
def total_posts_by_user(user):

    return Post.objects.filter(status='PB', author=user).count()

@register.simple_tag
def total_comments_by_user(user):

    return Comment.objects.filter(active=True, name=user).count()


@register.inclusion_tag('main/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status="PB").order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.filter(status='PB').annotate(
        total_comments=Count('comments')
    ).exclude(total_comments=0).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
