from django.urls import reverse
from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey

from myauth.models import User


class Post(models.Model):
    """
    Модель публикации
    """
    # class Status(models.TextChoices):
    #     DRAFT = 'DF', 'Draft'
    #     PUBLISHED = 'PB', 'Published'

    STATUS_OPTIONS = (
        ('PB', 'Опубликовано'),
        ('DF', 'Черновик')
    )

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
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default='PB')
    tags = TaggableManager()
    category = TreeForeignKey('Category',
                              on_delete=models.PROTECT,
                              related_name='posts',
                              verbose_name='Категория',
                              null=True,
                              blank=True)

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


class Category(MPTTModel):
    """
    Модель категорий
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    avatar = models.ImageField(upload_to='category_images', blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Название модели в админ панели, таблица с данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('post_by_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 40 or img.width > 40:
            new_img = (120, 120)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title
