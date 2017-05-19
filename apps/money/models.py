from django.db import models


class MoneyAccount(models.Model):
    STATUS_CHOICES = (('-1', '支出'), ('1', '收入'))
    TYPE_CHOICES = (('b', '银行'), ('c', '现金'))
    date = models.DateField('日期', null=False)
    detail = models.CharField('项目', null=False, max_length=120)
    status = models.CharField('去向', choices=STATUS_CHOICES, max_length=1, null=False)
    type = models.CharField('账目类型', choices=STATUS_CHOICES, max_length=1, null=False)
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
        last = MoneyAccount.objects.filter(date__lt=self.date)[0]
        if last:
            return self.amount * int(self.status) + last.get_balance
        return self.amount * int(self.status)
