from django.urls import reverse
from django.utils import timezone
from myauth.models import User
from django.db import models
from taggit.managers import TaggableManager


# class User(models.Model):
#     name = models.CharField(max_length=32, verbose_name="Имя пользователя")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ('-created_at',)
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#         get_latest_by = ['created_at']


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    def get_absolute_url(self):
        return reverse('showpost',
                       args=[self.slug])

    slug = models.SlugField(max_length=250, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

