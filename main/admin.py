from django.contrib import admin
from main.models import Post, Comment

# Register your models here.
admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'name', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
