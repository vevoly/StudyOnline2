# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 7:18'

import re
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile, EmailVerifyRecord


class RegisterForm(forms.Form):
    """
    注册
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class LoginForm(forms.Form):
    """
    登录
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    """
    忘记密码
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    def clean_email(self):
        """
        查找是否有输入的邮箱
        如果没有此邮箱，返回错误。
        :return:
        """
        email = self.cleaned_data['email']
        users = UserProfile.objects.filter(email=email)
        if users.count() == 0:
            raise forms.ValidationError('无此邮箱账号！', code='email_invalid')
        else:
            user = users[0]
            if user.is_active == 0:
                raise forms.ValidationError('账号尚未激活，请先激活！', code='email_invalid')
            return email


class UserInfoForm(forms.ModelForm):
    """
    用户中心-个人信息
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']

    def clean_mobile(self):
        """
        验证手机号是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        reg_pattern = '^1[358]\d{9}$|^147\d{8}|^176\d{8}$'
        p = re.compile(reg_pattern)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('非法手机号码', code='mobile_invalid')


class UpdateAvatarForm(forms.ModelForm):
    """
    个人中心-修改头像
    """
    class Meta:
        model = UserProfile
        fields = ['avatar']


class UpdatePasswordForm(forms.Form):
    """
    个人中心-修改密码
    """
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)

    def clean(self):
        """
        验证两次密码是否一致
        :return:
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2
        else:
            raise forms.ValidationError('两次密码输入不一致！', code='password2_invalid')


class UpdateEmailCodeForm(forms.Form):
    """
    个人中心-修改邮箱-发送验证码
    """
    email = forms.EmailField(required=True)


class UpdateEmailForm(UpdateEmailCodeForm):
    """
    个人中心-修改邮箱
    """
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        email = self.cleaned_data['email']
        code = self.cleaned_data['code']
        # 数据库中是否有code
        records = EmailVerifyRecord.objects.filter(email=email, send_type='upd_email', code=code)
        if records.count() == 0:
            raise forms.ValidationError('验证码有错', code='code_invalid')
        return code



