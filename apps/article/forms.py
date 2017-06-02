# _*_ conding:utf-8 _*_
__author__ = 'pbpoon'
__date__ = '2017/5/13 21:41'

from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '我来说两句~', 'row': 3})
        }


class ArticleEditForm(forms.ModelForm):
    tag_list = forms.ModelMultipleChoiceField(required=False, queryset=Article.tag.all(),)

    class Meta:
        model = Article
        fields = ['publish', 'title', 'content', 'tag']

    def __init__(self, *args, **kwargs):
        # super(self.__class__, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['tag_list'] = [(x.name, x.name) for x in Article.tag.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self,False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.tag.clear()
            tag = self.cleaned_data['tag']
            tag_list = self.cleaned_data['tag_list']
            # tags = tag + tag_list
            # tags =Tag.objects.filter(id__in=tags)
            for _tag in tag:
                instance.tag.add(_tag)
            for _tag in tag_list:
                instance.tag.add(_tag)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance