from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    bind_people = models.ForeignKey('account.People', null=True, related_name='user_profile', verbose_name='绑定村民信息')
    telephone = models.CharField('电话号码', null=True, blank=True, max_length=11)
    image = models.ImageField('头像图片', max_length=100, upload_to='image/Y%m%d%/', default='image/user.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username