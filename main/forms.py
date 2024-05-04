from django import forms

from .models import Comment, Post


# class PostForm(forms.Form):
#     title = forms.CharField(
#         label="Заголовок",
#         min_length=2,
#         max_length=64,
#         error_messages={'required': 'Please'},
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#     )
#     body = forms.CharField(
#         label="Пост",
#         widget=forms.Textarea(attrs={'class':"form-control"}),
#         error_messages={'required':'Ошибка, не введено сообщение'},
#     )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'body']
        labels = {'tags': 'Тэги'}
        help_texts = {'tags': ""}

        widgets = {
            "title": forms.TextInput(attrs={'class': "form-control"}),
            "body": forms.Textarea(attrs={'class': "form-control"}),
            "tags": forms.TextInput(attrs={'class': "form-control", 'placeholder': 'через запятую'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {"body": ''}
        widgets = {
            "body": forms.Textarea(attrs={'class': "form-control"}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
