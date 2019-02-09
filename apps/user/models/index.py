# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/2/9 0009 下午 9:07'

from django.db import models

from StudyOnline2.settings import BANNER_UPLOAD


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
