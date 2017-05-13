from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from .models import Article, Tag, Like
from .forms import CommentForm, LikeForm
import markdown


class ArticleListView(ListView):
    template_name = 'article/index.html'
    queryset = Article.objects.filter(publish=True)

    # def get_queryset(self):
    #     object_list = super(ArticleListView, self).get_queryset()
    #     for qs in object_list:
    #         qs.content = markdown.markdown(qs.content)
    #     return object_list

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context


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
        context['comment_list'] = self.object.comment.all()
        context['form'] = CommentForm()

        return context


class TagListView(ListView):
    template_name = 'article/index.html'

    def get_queryset(self):
        object_list = Article.objects.filter(publish=True, tag__in=self.kwargs['tag_id'])
        return object_list

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context


class CommentView(FormView):
    template_name = 'article/comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = article
        comment.user = self.request.user
        comment.save()
        self.success_url = article.get_absolute_url()

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        context = {
            'form': form,
            'comment_list': article.comment.all(),
            'object': article
        }

        return render(self.request, 'article/detail.html', context)

class ClickLikeView(FormView):
    template_name = ''
    form_class = LikeForm

    def form_valid(self, form):
        pass

