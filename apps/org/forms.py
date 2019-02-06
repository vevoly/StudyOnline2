# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/29 0029 上午 9:54'

import re
from django import forms

from operation.models import UserAsk


class AddUserAskForm(forms.ModelForm):
    """
    添加用户咨询
    """
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        reg_pattern = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(reg_pattern)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码格式错误', code='mobile_invalid')


