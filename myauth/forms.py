from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            if field_name == 'password2':
                # field.widget = HiddenInput()
                field.widget.attrs['class'] = 'form-control'
                field.required = False

