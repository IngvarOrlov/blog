from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from main.models import Post, Comment, Category

# Register your models here.
admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'name', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}