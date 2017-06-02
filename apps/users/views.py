from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import View, TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from article.models import Article
from account.models import Account, People

from .models import UserProfile
from .forms import LoginForm, RegisterForm


class CustomAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(bind_people__first_name=username[:1],
                                                                    bind_people__last_name=username[1:]))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#
# class LoginView(View):
#     template_name = 'login.html'
#     def post(self, request):
#
#         form = LoginForm(request.POST)
#         data = {}
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd.get('user_name'), password=cd.get('password'))
#             if user is not None:
#                 login(request, user)
#                 # return HttpResponseRedirect(reverse('article:index'))
#                 return HttpResponseRedirect(request.POST['next'])
#             msg = '用户名或者密码错误!'
#             return render(request, self.template_name, locals())
#         else:
#             return render(request, self.template_name, locals())
#
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'login.html', locals())


# class LogoutView(View):
#
#     def get(self, request):
#         logout(request)
#         return HttpResponseRedirect(reverse('article:index'))


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    def form_valid(self, form):
        '''
        创建用户并绑定村民信息
        '''
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        bind_people = form.cleaned_data['people_name']

        new_user = UserProfile.objects.create(username=username, bind_people=bind_people)
        new_user.set_password(password)
        new_user.save()
        '''如注册资料有电话号码,保存电话号码到people的资料'''
        telphone = form.cleaned_data['telphone']
        if telphone:
            bind_people.phone_num = telphone
            bind_people.save()
        return render(self.request, 'registration/login.html', {'msg': '注册成功!', 'form': form})
    # return render(request, 'registration/register.html', {'form': form})


class UserInfolView(View):
    template_name = 'user_info.html'

    def get(self, request, pk):
        user = get_object_or_404(UserProfile, pk=pk)

        context = {
            'user': user
        }
        return render(request, self.template_name, context)


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        if q:
            context['list'] = {}

            article_list = Article.objects.filter(
                Q(Q(title__icontains=q) |
                  Q(content__icontains=q)
                  ) |
                Q(Q(tag__name__icontains=q) |
                  Q(
                      Q(author__bind_people__first_name__icontains=q) |
                      Q(author__bind_people__last_name__icontains=q)))

            ).distinct()

            account_list = Account.objects.filter(
                Q(name__icontains=q) |
                Q(
                    Q(people__last_name__icontains=q) |
                    Q(people__phone_num__icontains=q))
            ).distinct()

            people_list = ''

            if self.request.user.is_superuser:
                people_list = People.objects.filter(
                    Q(first_name__icontains=q) |
                    Q(
                        Q(last_name__icontains=q) |
                        Q(phone_num__icontains=q))
                ).distinct()

        if article_list or people_list or account_list:

            context['list'] = {
                'article_list': article_list,
                'account_list':account_list,
                'people_list': people_list,
                'count':len(article_list)+len(people_list) + len(account_list)
            }

        else:
            context['msg'] = '没有相关的搜索内容！'

        return context
