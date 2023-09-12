from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['headline', 'text', 'category', 'to_author']


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['headline', 'text', 'category', 'to_author']


# class NewsForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['headline', 'text', 'category', 'to_author']

