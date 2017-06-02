# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/6/1 11:35'

from django import template
from ..models import Article
from django.db.models import Count
from django.utils.safestring  import mark_safe
import markdown
import datetime

register = template.Library()


@register.simple_tag
def total_article():
    return Article.objects.filter(publish=True).count()


@register.inclusion_tag('article/last_article.html')
def show_last_article(count=5):
    last_article = Article.objects.order_by('-create_d')[:count]
    return {'last_article': last_article}


@register.inclusion_tag('article/most_comment_article.html')
def show_most_comment_article(count=5):
    most_comment_article = Article.objects.filter(publish=True).annotate(most_comment=Count('comment')).order_by(
        '-most_comment')[:count]
    return {'most_comment_article': most_comment_article}


@register.inclusion_tag('article/tag_list.html')
def show_tag_list():
    tag_list = Article.tag.all()
    return {'tag_list': tag_list}


@register.filter(name='markdown')
def markdown_fornat(text):
    return mark_safe(markdown.markdown(text))