from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MoneyAccount(models.Model):
    STATUS_CHOICES = (('-1', '支出'), ('1', '收入'))
    TYPE_CHOICES = (('b', '银行'), ('c', '现金'))
    date = models.DateField('日期', null=False, default=datetime.date.today())
    detail = models.CharField('项目', null=False, max_length=120)
    status = models.CharField('去向', choices=STATUS_CHOICES, max_length=2, null=False)
    type = models.CharField('账目类型', choices=TYPE_CHOICES, max_length=1, null=False)
    amount = models.DecimalField('金额', decimal_places=2, max_digits=9, null=False)
    operator = models.ForeignKey('users.UserProfile', verbose_name='经手人')
    ps = models.CharField('备注说明', max_length=200, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '银行流水账'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return '{0}/{1}/{2}'.format(self.date, self.detail, self.amount)

    def save(self, *args, **kwargs):
        if self.status == '-1':
            self.amount = -(self.amount)
        super(MoneyAccount, self).save(*args, **kwargs)

    @property
    def get_balance(self):
        lst = MoneyAccount.objects.all()
        for last in lst:
            try:
                count = MoneyAccount.objects.filter(date=last.date)
                if len(count) > 1:
                    try:
                        c = count.filter(id__lt=self.id)[0]
                        if c:
                            return self.amount + c.get_balance
                    except:
                        return self.amount
                else:
                    try:
                        c = last.filter(date__lt=self.date)[0]
                        if c:
                            return self.amount + c.get_balance
                    except:
                        return self.amount
            except:
                try:
                    c = MoneyAccount.objects.filter(date__lt=last.date)[0]
                    if c:
                        return self.amount + c.get_balance
                except:
                    return self.amount




