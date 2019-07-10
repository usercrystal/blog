from django import forms

from .models import ArticleColumn1, ArticlePost1, Comment
from django.contrib.auth.models import User


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn1
        fields = ['column']


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost1
        fields = ['title', 'body']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']