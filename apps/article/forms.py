#_*_ conding:utf-8 _*_
__author__ = 'pbpoon'
__date__ = '2017/5/13 21:41'

from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment':forms.Textarea(attrs={'class': 'form-control', 'placeholder': '我来说两句~', 'row':3})
        }


# class ArticleEditForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['publish', 'title', 'content', 'tag']
#         widgets = {
#             'tag': TagField(widget=taggit_bootstrap.TagsInput)
#         }