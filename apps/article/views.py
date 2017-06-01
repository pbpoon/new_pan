from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, View, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, Tag, Like
from .forms import CommentForm

import markdown
from django.http import JsonResponse


class AuthorMixin:
    '''
    把author在query裏篩選出來
    '''
    def get_queryset(self):
        qs = super(AuthorMixin, self).get_queryset()
        return qs.filter(author=self.request.user)


class AuthorArticleMixin(AuthorMixin):
    '''
    定好要使用的model
    '''
    model = Article


class AuthorEditMixin:
    '''
    把需要用到表单的view最后把author加上为当前用户
    '''
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AuthorEditMixin, self).form_valid(form)


class ArticleEditMixin(LoginRequiredMixin, AuthorArticleMixin, AuthorEditMixin):
    fields = ['title', 'content', 'tag', 'publish']
    success_url = reverse_lazy('article:index')
    template_name = 'article/form.html'


class ArticleCreateView(ArticleEditMixin, CreateView):
    pass


class ArticleUpdateView(ArticleEditMixin, UpdateView):
    pass


class ArticleDelteView(ArticleEditMixin, UpdateView):
    pass


class ArticleListView(ListView):
    template_name = 'article/index.html'
    queryset = Article.objects.filter(publish=True)
    paginate_by = 12

    def get_queryset(self):
        publish = self.request.GET.get('publish', True)
        kwarg = {'publish': publish}
        return Article.objects.filter(**kwarg)

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Article.tag.all()
        return super(ArticleListView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    template_name = 'article/detail.html'
    model = Article

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.content = markdown.markdown(obj.content)

        return obj

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = self.object.tag.all()
        kwargs['form'] = CommentForm()
        kwargs['article_like'] = [obj.user for obj in Like.objects.filter(type='a', like_id=self.object.id, like=True)]
        kwargs['article_unlike'] = [obj.user for obj in Like.objects.filter(type='a', like_id=self.object.id, like=False)]
        all_comment = self.object.comment.all()

        '''
        新建一个kwargs的字典项，并遍历评论的queryset，把点击状态，点击量等添加到该字典项
        '''
        kwargs['comment_list'] = {}
        for comment in all_comment:
            comment_id = str(comment.id)
            like = [obj.user for obj in Like.objects.filter(type='c', like_id=comment_id, like=True)]
            unlike = [obj.user for obj in Like.objects.filter(type='c', like_id=comment_id, like=False)]
            kwargs['comment_list'][comment_id] = {
                'comment': comment,
                'like': like,
                'unlike': unlike,
            }

        return super(ArticleDetailView, self).get_context_data(**kwargs)


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


class LikeView(View):
    def get(self, request):
        article = Article.objects.get(id=self.request.GET.get('article_id'))
        like_id = self.request.GET.get('like_id')
        type = self.request.GET.get('type')
        like = self.request.GET.get('like')
        '''
        只有登陆的用户点赞才能有效
        '''
        if self.request.user.is_authenticated:
            try:
                liked = Like.objects.get(type=type, like_id=like_id, user=self.request.user)
            except:
                Like.objects.create(type=type, like_id=like_id, like=like, user=self.request.user)
            else:
                liked.like = like
                liked.save()
            A = '文章' if type == 'a' else '评论'
            B = '点赞' if like == 'True' else '发表不满'
            if like == 'True':
                messages.success(request, '你已对该{0}{1}!'.format(A, B))
            else:
                messages.warning(request, '你已对该{0}{1}!'.format(A, B))
        #     like_count = {'like_count':Like.objects.filter(type=type, like_id=like_id, like=like).count()}
        # return JsonResponse(like_count)
        return redirect(article.get_absolute_url())
