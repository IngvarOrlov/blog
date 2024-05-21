from django import forms

from .models import Comment, Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'category', 'body']
        labels = {'tags': 'Тэги'}
        help_texts = {'tags': ""}

        widgets = {
            "title": forms.TextInput(attrs={'class': "form-control"}),
            # "body": forms.Textarea(attrs={'class': "form-control django_ckeditor_5", 'cols': 60}),
            "tags": forms.TextInput(attrs={'class': "form-control", 'placeholder': 'через запятую'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
            self.fields['body'].widget.attrs.update({'class': 'form-control django_ckeditor_5', 'cols':60})



class CommentForm(forms.ModelForm):
    """
        Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Comment
        fields = ['body', 'parent']
        labels = {"body": ''}
        widgets = {
            "body": forms.Textarea(attrs={'class': "form-control",
                                          'cols': 30,
                                          'rows': 5,
                                          'placeholder': 'Комментарий',
                                          }),

        }




class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'поиск..'}))