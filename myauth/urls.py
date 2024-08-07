from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from blog import settings
from myauth.views import *

app_name = 'myauth'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('register/', MyUserCreateView.as_view(), name='register'),
    # path('profile/', profile, name='profile_edit'),
    path('profile/', ProfileUpdate.as_view(), name='profile_edit'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile_view'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    # path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
]
