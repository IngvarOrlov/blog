from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from myauth.models import User

class MyUserAdmin(UserAdmin):
    pass

admin.site.register(User, MyUserAdmin)