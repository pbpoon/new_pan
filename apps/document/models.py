from django.shortcuts import reverse
from django.db import models
import os


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField('名称', max_length=20, db_index=True)
    desc = models.CharField('描述', max_length=60, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)
    category = models.ForeignKey('Category', related_name='document', verbose_name='分类名称')
    views = models.IntegerField('查阅量', default=0)

    class Meta:
        verbose_name = '档案名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def _get_item_count(self):
        return self.item.count()
    _get_item_count.short_description = '文件数'
    item_count = property(_get_item_count)

    def get_absolute_url(self):
        return reverse('document:detail', kwargs={'pk': self.id})


def get_upload_to(instance, filename):
    return 'document/{0}/{1}'.format(instance.document, filename)


class DocumentItem(models.Model):
    document = models.ForeignKey('Document', related_name='item', verbose_name='分类名称')
    name = models.CharField('名称', max_length=20, null=True, blank=True)
    file = models.FileField('文件', upload_to=get_upload_to)
    desc = models.CharField('描述', max_length=60, null=True, blank=True)
    format = models.CharField('文件格式', max_length=12, default='jpg')
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '档案名称'
        verbose_name_plural = verbose_name

    def save(self):
        super(DocumentItem, self).save()
        _name, _format = os.path.splitext(os.path.basename(self.file.path))
        if not self.name:
            self.name = _name
        self.format = _format.lstrip('.')
        super(DocumentItem, self).save()

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return reverse('document:item_detail', kwargs={'pk': self.id})


