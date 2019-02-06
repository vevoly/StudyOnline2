from django.db import models


from user.models import UserProfile
from course.models import Course
from utils.choices import fav_type_choices


class UserAsk(models.Model):
    """
    用户咨询
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.course_name, self.name)


class Comment(models.Model):
    """
    课程评论
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='评论课程')
    comment = models.CharField(max_length=200, verbose_name='评论内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.course.name, self.user.username)


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_type = models.SmallIntegerField(choices=fav_type_choices, default=1, verbose_name='收藏类型')
    fav_id = models.IntegerField(default=0, verbose_name='收藏数据ID')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s-%s (%s)' % (self.fav_id, self.fav_type, self.user.username)


class UserMessage(models.Model):
    """
    用户消息
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    message = models.CharField(max_length=500, default='', verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否阅读')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserCourse(models.Model):
    """
    用户学习过的课程
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户学习过的课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.course.name, self.user.username)


