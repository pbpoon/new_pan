# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/5/6 15:27'

from django import forms
from .models import UserProfile
from account.models import People

class LoginForm(forms.Form):
    user_name = forms.CharField(label='账号', required=True, min_length=5)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', help_text='用于登录的账户名称', required=True, min_length=8, max_length=18)
    password = forms.CharField(label='设置密码', help_text='用于登录的密码', required=True, min_length=8,
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='重新输入密码', help_text='用于登录的密码', required=True, min_length=8,
                                widget=forms.PasswordInput)
    people_name = forms.CharField(label='本村户口内姓名', help_text='账户绑定的本村户口姓名，必须正确', required=True, min_length=2)
    # card_num = forms.CharField(label='身份证号码', help_text='账户绑定的本村户口姓名的身份证号码', required=True, min_length=2)

    card_num = forms.CharField(label='身份证号码',  help_text='账户绑定的本村户口姓名的身份证号码', required=True, widget=forms.TextInput)
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不相等！')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username or '@' in username:
            raise forms.ValidationError(u'昵称中不能包含空格和@字符')
        res = UserProfile.objects.filter(username=username)
        if len(res) != 0:
            raise forms.ValidationError(u'此昵称已经注册，请重新输入')
        return username

    # def clean_idcard_num(self):
    #     cd = self.cleaned_data
    #     return cd['idcard_num']

    def clean_people_name(self):
        people_name = self.cleaned_data['people_name']
        card_num = self.cleaned_data.get('card_num')
        people = People.objects.get(first_name=people_name[:1], last_name=people_name[1:], id_card_num=card_num)
        if people is None:
            raise forms.ValidationError(u'输入的村民姓名或身份证号码有误，请重新输入！')
        else:
            if UserProfile.objects.get(bind_people=people).exists():
                raise forms.ValidationError(u'输入的村民姓名已注册账户！')
        return people

    # def save(self, commit=True):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password2']
    #
    #     new_user = UserProfile.objects.all()



