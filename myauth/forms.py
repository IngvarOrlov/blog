from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import HiddenInput

from myauth.models import User


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
