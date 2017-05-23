from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField('档案名称')
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)
    category = models.ForeignKey('Category', related_name='file', verbose_name='分类名称')
    file = models.ManyToManyField('File', related_name='album', verbose_name='文件')


class File(models.Model):
    title = models.CharField('标题', max_length=40, null=True, blank=True)
    desc = models.CharField('描述', max_length=200, null=True, blank=True)
    path = models.FileField('路径', upload_to='file/%Y%m%d')
    format = models.CharField('文件类型', max_length=20, default='.jpg')
    update_d = models.DateTimeField('更新日期', auto_now=True)