# _*_ conding:utf-8 _*_
__author__ = 'pbpoon'
__date__ = '2017/6/2 21:25'

from django import template
from ..models import People, Account
from decimal import Decimal

register = template.Library()


@register.inclusion_tag('account/sidebar.html')
def show_sidebar():
    context = {}
    account = Account.objects.filter(people__is_del=False).distinct()
    peoples = People.objects.filter(is_del=False)
    context['total_people'] = peoples.count()
    context['total_get_getmoney'] = peoples.filter(is_getmoney=True).count()
    context['average_age'] = Decimal(sum(people.get_age for people in peoples) \
                                     / peoples.count()).quantize(Decimal('0.0'))
    context['total_male'] = peoples.filter(sex='male').count()
    context['total_female'] = peoples.filter(sex='female').count()
    context['male_to_female'] = Decimal(1 / (context['total_male'] / context['total_female'])).quantize(
        Decimal('0.00'))
    context['min_65_age_total'] = len([people for people in peoples if people.get_age > 65])
    context['min_65_age_male'] = len([people for people in peoples.filter(sex='male') if people.get_age > 65])
    context['min_65_age_female'] = len([people for people in peoples.filter(sex='female') if people.get_age > 65])
    context['betwee_18_to_45_total'] = len(
        [people for people in peoples if people.get_age < 45 and people.get_age > 18])
    context['betwee_18_to_45_male'] = len(
        [people for people in peoples.filter(sex='male') if people.get_age < 45 and people.get_age > 18])
    context['betwee_18_to_45_female'] = len(
        [people for people in peoples.filter(sex='female') if people.get_age < 45 and people.get_age > 18])
    context['account_count'] = len(account)
    return context
