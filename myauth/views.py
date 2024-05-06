from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from myauth.forms import MyUserCreateForm, LoginForm
from myauth.models import User


# Create your views here.
class MyUserCreateView(CreateView):
    model = User
    success_url = reverse_lazy("login")
    form_class = MyUserCreateForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(MyUserCreateView, self).dispatch(request, *args, **kwargs)

class Login(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    success_message = "Вы вошли как %(username)s"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(Login, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(Login, self).dispatch(request, *args, **kwargs)

class Logout(SuccessMessageMixin, LogoutView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли успешно")
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    return render(request, 'myauth/profile.html')