from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic import CreateView, View, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction

from myauth.forms import MyUserCreateForm, LoginForm, UpdateUserForm, UpdateProfileForm
from myauth.models import User, Profile


# Create your views here.
class MyUserCreateView(CreateView):
    model = User
    success_url = reverse_lazy("login")
    form_class = MyUserCreateForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect(to='/')
            return redirect(reverse_lazy('profile_view', kwargs={'pk': self.request.user.pk}))
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


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=request.user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Ваш профиль успешно изменен')
#             return redirect(to='profile_view', pk=request.user.pk)
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=request.user.profile)
#     return render(request, 'myauth/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'myauth/change_password.html'
    success_message = "Вы сменили пароль"
    def get_success_url(self):
        return reverse_lazy('profile_view', kwargs={'pk': self.request.user.pk})


class ProfileView(DetailView):
    model = User
    template_name = "myauth/profile_detail.html"
    context_object_name = "profile"



class ProfileUpdate(UpdateView):
    model = Profile
    template_name = "myauth/prof_update.html"
    form_class = UpdateProfileForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UpdateUserForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UpdateUserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
                messages.success(self.request, 'Ваш профиль успешно изменен')
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('profile_view', kwargs={'pk': self.object.user.pk})


