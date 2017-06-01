# _*_ conding:utf-8 _*_
__author__ = 'pbpoon'
__date__ = '2017/5/13 21:41'

from django import forms
from .models import Comment, Article
from markdownx.fields import MarkdownxFormField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '我来说两句~', 'row': 3})
        }


class ArticleEditForm(forms.ModelForm):
    tag_list = forms.MultipleChoiceField(required=False)
    class Meta:
        model = Article
        fields = ['publish', 'title', 'content', 'tag']

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['tag_list'].choices = ((x.id, x.name) for x in Article.tag.all())

    def save(self, commit=True):
        article = super(self.__class__, self).save(commit=True)
        if self.fields['tag']:
            if self.fields['tag'] in self.fields['tag_list']:
                article.tag.add(self.tag_list)
            else:
                article.tag.add(self.tag)
        super(self.__class__, self).save(commit=True)
