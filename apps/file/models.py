from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
