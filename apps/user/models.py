from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.choices import gender_choices, send_type_choices
from StudyOnline2.settings import USER_UPLOAD, BANNER_UPLOAD


class UserProfile(AbstractUser):
    """
    用户
    """
    USER_AVATAR = USER_UPLOAD.get('AVATAR')
    nick_name = models.CharField(max_length=50, verbose_name='昵称', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=6, choices=gender_choices, default=gender_choices[0][0], verbose_name='性别')
    address = models.CharField(max_length=100, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机')
    avatar = models.ImageField(upload_to=USER_AVATAR.get('UPLOAD'), max_length=100,
                               default=USER_AVATAR.get('DEFAULT'), verbose_name='头像')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self):
        """
        未读消息条数
        :return:
        """
        return self.usermessage_set.filter(is_read=0).count()


class EmailVerifyRecord(models.Model):
    """
    电子邮件验证码记录
    """
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='电子邮箱')
    send_type = models.CharField(choices=send_type_choices, verbose_name='发送类型', max_length=10)
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.code, self.email)


class Banner(models.Model):
    """
    轮转图
    """
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to=BANNER_UPLOAD.get('INDEX'), verbose_name='图片')
    url = models.URLField(max_length=200, verbose_name='图片地址')
    index = models.SmallIntegerField(default=100, verbose_name='轮转图顺序')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.title, self.index)



