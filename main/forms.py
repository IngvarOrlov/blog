from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        label="Заголовок",
        min_length=2,
        max_length=64,
        error_messages={'required': 'Please'},
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    body = forms.CharField(
        label="Пост",
        widget=forms.Textarea(attrs={'class':"form-control"}),
        error_messages={'required':'Ошибка, не введено сообщение'},
    )


