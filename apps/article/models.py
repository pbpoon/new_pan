from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField('作者', max_length=20)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('标题', max_length=120)
    content = models.TextField('内容')
    author = models.ForeignKey('Author', related_name='article', verbose_name='作者')
    tag = models.ManyToManyField('Tag', related_name='article', verbose_name='标签')
    likes = models.IntegerField('点赞数', default=0)
    views = models.IntegerField('浏览数', default=0)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_d']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField('名称', max_length=20)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    commnet = models.CharField('评论内容', max_length=200)
    name = models.CharField('姓名', max_length=20)
    likes = models.IntegerField('点赞数', default=0)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_d']

    def __str__(self):
        return self.commnet[:20]