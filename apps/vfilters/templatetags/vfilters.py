from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='plus_years', is_safe=True)
@stringfilter
def plus_years(value):
    """
    在字符串后加年
    :param value:
    :return:
    """
    return mark_safe('%s年' % value)
