from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from myauth.views import MyUserCreateView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', MyUserCreateView.as_view(), name='register'),
]
