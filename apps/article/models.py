from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField('分类名称', max_length=20, db_index=True)
    desc = models.CharField('分类描述', max_length=60, null=True, blank=True)

    class Meta:
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('标题', max_length=120)
    content = models.TextField('内容')
    author = models.ForeignKey('users.UserProfile', related_name='article', verbose_name='作者')
    tag = models.ManyToManyField('Tag', related_name='article', verbose_name='标签')
    views = models.IntegerField('浏览数', default=0)
    publish = models.BooleanField('发布', default=False)
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_d']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail', kwargs={'pk': self.pk})


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
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comment', verbose_name='文章')
    comment = models.CharField('评论内容', max_length=200)
    user = models.ForeignKey('users.UserProfile', related_name='article_comment', verbose_name='用户')
    create_d = models.DateTimeField('创建时间', auto_now_add=True)
    update_d = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_d']

    def __str__(self):
        return "{0}:{1}...".format(self.article, self.commnet[:20])


class Like(models.Model):
    type = models.CharField('点赞类型', max_length=1, choices=(('a', '文章'), ('c', '评论')), default='a')
    like_id = models.IntegerField('点赞类型的id')
    like = models.BooleanField('点赞', default=True)
    user = models.ForeignKey('users.UserProfile', related_name='like', verbose_name='用户')
    create_d = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_d']

