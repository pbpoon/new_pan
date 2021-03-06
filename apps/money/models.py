from django.db import models
from django.shortcuts import reverse
from collections import defaultdict


class MoneyAccountManager(models.Manager):
    def date_objects(self):
        date_list = MoneyAccount.objects.dates('date', 'month')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items())


class Tag(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MoneyAccount(models.Model):
    STATUS_CHOICES = (('-1', '支出'), ('1', '收入'))
    TYPE_CHOICES = (('b', '银行'), ('c', '现金'))

    num = models.IntegerField('序号', default=0)
    date = models.DateField('日期', null=False)
    detail = models.CharField('项目', null=False, max_length=120)
    status = models.CharField('去向', choices=STATUS_CHOICES, max_length=2, null=False)
    type = models.CharField('账目类型', choices=TYPE_CHOICES, max_length=1, null=False)
    amount = models.DecimalField('金额', decimal_places=2, max_digits=9, null=False)
    operator = models.ForeignKey('users.UserProfile', verbose_name='经手人')
    ps = models.CharField('备注说明', max_length=200, null=True, blank=True)
    tag = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)
    objects = MoneyAccountManager()

    class Meta:
        verbose_name = '流水账'
        verbose_name_plural = verbose_name
        ordering = ['type', 'num']

    def __str__(self):
        return '{0}/{1}/{2}'.format(self.date, self.detail, self.amount)

    def save(self, *args, **kwargs):
        if self.num == 0:
            last_num = MoneyAccount.objects.filter(type=self.type).last()
            self.num = last_num.num + 1
        if self.status == '-1':
            self.amount = -(self.amount)
        super(MoneyAccount, self).save(*args, **kwargs)

    @property
    def get_balance(self):
        alls = MoneyAccount.objects.filter(num__lt=self.num, type=self.type)
        return self.amount + sum(item.amount for item in alls if item.type == self.type)

    def get_absolute_url(self):
        return reverse('money:item_detail', kwargs={'pk': self.id})


class Document(models.Model):
    img = models.ImageField('留档图片', upload_to='file/money/%Y%m%d', max_length=120)
    money_num = models.ForeignKey('MoneyAccount', related_name='doc', null=False, on_delete=models.CASCADE, verbose_name='对应账款')
    desc = models.CharField('图片说明', max_length=200, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)


    class Meta:
        verbose_name = '流水账留档图片'
        verbose_name_plural = verbose_name
        ordering = ['create_d']

    def __str__(self):
        return self.desc[:20]

