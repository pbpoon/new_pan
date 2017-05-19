from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic import ListView, DetailView, FormView, View
from django.contrib import messages

from .models import Article, Tag, Like
from .forms import CommentForm

import markdown


class ArticleListView(ListView):
    template_name = 'article/index.html'
    queryset = Article.objects.filter(publish=True)
    paginate_by = 12

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
        context['form'] = CommentForm()
        context['article_like'] = Like.objects.filter(type='a', like_id=self.object.id, like=True).count()
        context['article_unlike'] = Like.objects.filter(type='a', like_id=self.object.id, like=False).count()
        '''判断有没有点过like或unlike，默认false'''
        context['is_click'] = False
        '''判断like或unlike'''
        context['liked'] = False

        '''如果是登陆的用户，就判断其在本article的like状态，先查找有没有有记录，如果有就进一步判断
        并把点击状态改变'''
        if self.request.user.is_authenticated:
            try:
                liked = Like.objects.get(type='a', like_id=self.object.id, user=self.request.user)
            except:
                pass
            else:
                context['is_click'] = True
                context['liked'] = liked.like
        all_comment = self.object.comment.all()

        '''
        新建一个context的字典项，并遍历评论的queryset，把点击状态，点击量等添加到该字典项
        '''
        context['comment_list'] = {}
        for comment in all_comment:
            comment_id = str(comment.id)
            like = Like.objects.filter(type='c', like_id=comment_id, like=True).count()
            unlike = Like.objects.filter(type='c', like_id=comment_id, like=False).count()
            is_click = False
            liked = False

            print(comment.id)
            if self.request.user.is_authenticated:
                try:
                    cliked = Like.objects.get(type='c', like_id=comment.id, user=self.request.user)
                except:
                    pass
                else:
                    is_click = True
                    liked = cliked.like
                finally:
                    context['comment_list'][comment_id] = {
                        'comment': comment,
                        'like': like,
                        'unlike': unlike,
                        'is_click': is_click,
                        'liked': liked,
                    }

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
            B = '点赞' if like=='True' else '发表不满'
            if like == 'True':
                messages.success(request, '你已对该{0}{1}!'.format(A, B))
            else:
                messages.warning(request, '你已对该{0}{1}!'.format(A, B))
        return redirect(article.get_absolute_url())
