from django.db import models
from django.shortcuts import reverse
from datetime import date


class PeopleNoDelManager(models.Manager):
    def get_queryset(self):
        return super(PeopleNoDelManager, self).get_queryset().filter(is_del=False)


class Account(models.Model):
    name = models.CharField('户名号码', unique=True, db_index=True, max_length=12)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '户口号码'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("account:detail", kwargs={'name':self.name})

    def __str__(self):
        if self.people.filter(is_main=True).exists():
            return "{0}:{1}".format(self.name, self.people.get(is_main=True))
        return "{0}".format(self.name)

    __repr__ = __str__

    def get_peolpe_count(self):
        return self.people.filter(is_del=False).count()

    def get_getmoney_count(self):
        return self.people.filter(is_getmoney=True, is_del=False).count()


class People(models.Model):
    SEX_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    first_name = models.CharField('姓氏', max_length=8)
    last_name = models.CharField('名字', max_length=12)
    sex = models.CharField('性别', choices=SEX_CHOICES, max_length=6)
    id_card_num = models.CharField('身份证号码', db_index=True, max_length=18, null=True, blank=True)
    is_main = models.BooleanField('是否为户主', default=False)
    account = models.ForeignKey('Account', related_name='people', null=True, blank=True, verbose_name='所属户口')
    birthday = models.DateField('出生日期', null=True, blank=True)
    is_marry = models.BooleanField('是否已婚', default=False)
    is_getmoney = models.BooleanField('分钱资格', default=False)
    join_d = models.DateField('入户日期', null=True, blank=True)
    nationality = models.CharField('民族', null=True, blank=True, max_length=26)
    education = models.CharField('教育程度', null=True, blank=True, max_length=20)
    account_type = models.CharField('户口类型', null=True, blank=True, max_length=20)
    phone_num = models.CharField('电话号码', null=True, blank=True, max_length=11)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新日期', auto_now=True)
    is_del = models.BooleanField('是否注销', default=False)

    # objects = PeopleNoDelManager()
    # all_people = models.Manager()

    class Meta:
        verbose_name = '村民信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    __repr__ = __str__

    def get_age(self):
        today = date.today()
        try:
            birthday = self.birthday.replace(year=today.year)
        except ValueError:
            # raised when birth date is February 29
            # and the current year is not a leap year
            birthday = self.birthday.replace(year=today.year, day=self.birthday.day - 1)
        if birthday > today:
            return today.year - self.birthday.year - 1
        else:
            return today.year - self.birthday.year

    def get_absolute_url(self):
        return reverse("account:people", kwargs={'pk': self.id})

    @property
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)