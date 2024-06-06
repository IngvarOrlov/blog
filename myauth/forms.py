from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import HiddenInput

from myauth.models import User, Profile


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {'username': 'Имя',
                  'email': 'Email',
                  'password1': 'Пароль',
                  'password2': 'Подтвердите пароль'
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        for field_name, field in self.fields.items():
            field.help_text = ''
            # if field_name == 'password2':
            #     # field.widget = HiddenInput()
            #     field.widget.attrs['class'] = 'form-control'
            #     field.required = False


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    w = forms.TextInput(attrs={"class": "form-control mb-1"})
    username = forms.CharField(max_length=100,
                               required=True,
                               label='Ник',
                               widget=w)
    first_name = forms.CharField(max_length=50,
                                 required=False,
                                 label='Имя',
                                 widget=w)
    last_name = forms.CharField(max_length=50,
                                 required=False,
                                 label='Фамилия',
                                 widget=w)

    email = forms.EmailField(required=True, label='E-mail',
                             widget=w)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар',
                              widget=forms.FileInput(attrs={"class": "form-control mb-1"}))
    bio = forms.CharField(label='О себе',
                          widget=forms.Textarea(attrs={'rows': 5, "class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']