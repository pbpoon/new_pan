from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import markdown


class ArticleListView(ListView):
    template_name = 'article/index.html'
    queryset = Article.objects.filter(publish=True)

    # def get_queryset(self):
    #     object_list = super(ArticleListView, self).get_queryset()
    #     for qs in object_list:
    #         qs.content = markdown.markdown(qs.content)
    #     return object_list


class ArticleDetailView(DetailView):
    template_name = 'article/detail.html'
    model = Article

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.content = markdown.markdown(obj.content)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['tag_list'] = self.object.tag.all()
        return context


class TagListView(ListView):
    template_name = 'article/index.html'

    def get_queryset(self):
        object_list = Article.objects.filter(publish=True, tag__in=self.kwargs['tag_id'])
        return object_list
