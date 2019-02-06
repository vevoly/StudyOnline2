# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 10:52'

from random import Random

from django.core.mail import send_mail

from user.models import EmailVerifyRecord
from StudyOnline2.settings import EMAIL_FROM


def random_str(random_lenght=8):
    """
    获取随机字符串
    :param random_lenght:
    :return:
    """
    str = ''
    char_set = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(char_set) - 1
    random = Random()
    for i in range(random_lenght):
        str += char_set[random.randint(0, length)]
    return str


def send_email(email, send_type='register'):
    """
    发送电子邮件
    :param email:
    :param send_type:
    :return:
    """
    verify_code = EmailVerifyRecord()
    if send_type == 'upd_email':
        verify_code.code = random_str(4)
    else:
        verify_code.code = random_str(16)
    verify_code.email = email
    verify_code.send_type = send_type
    verify_code.save()

    if send_type == 'register':
        email_title = "在线学校网激活链接"
        email_body = "请点击下面的链接激活你的帐号：http://127.0.0.1:8000/account/active/{0}".format(verify_code.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送注册激活邮件成功")
    elif send_type == 'forget':
        email_title = '在线学校网网密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/account/reset/{0}'.format(verify_code.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送重置密码邮件成功")
    elif send_type == 'upd_email':
        email_title = '在线学校网修改邮箱验证码'
        email_body = '你的邮箱验证码为：{0}'.format(verify_code.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print("发送修改密码验证邮件成功")
