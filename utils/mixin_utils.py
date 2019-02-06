# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/28 0028 下午 12:15'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

"""
需登录后才能访问
用以代替login_required装饰器
自定义View继承此类即可
例如：
xxxView(LoginRequiredMixin, View):
"""


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


