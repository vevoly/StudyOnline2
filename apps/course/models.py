from django.db import models

# Create your models here.

from DjangoUeditor.models import UEditorField

from org.models import Org, Teacher

from utils.choices import course_level_choices
from StudyOnline2.settings import COURSE_UPLOAD


class CourseCategory(models.Model):
    """
    课程类别
    """
    name = models.CharField(max_length=20, verbose_name='课程类别')
    index = models.SmallIntegerField(default=100, verbose_name='类别排序')

    class Meta:
        verbose_name = '课程类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    课程
    """
    COURSE_DETAIL = COURSE_UPLOAD.get('DETAIL')
    COURSE_COVER = COURSE_UPLOAD.get('COVER')

    org = models.ForeignKey(Org, verbose_name='所属机构')
    teacher = models.ForeignKey(Teacher, verbose_name='所属教师')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.TextField(verbose_name='课程描述')
    level = models.CharField(choices=course_level_choices, default=course_level_choices[0][0], max_length=20, verbose_name='课程等级')
    category = models.ForeignKey(CourseCategory, verbose_name='课程类别')
    detail = UEditorField(width=800, height=300, default='', imagePath=COURSE_DETAIL.get('IMAGE'),
                          filePath=COURSE_DETAIL.get('FILE'), verbose_name='课程详情')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    cover = models.ImageField(upload_to=COURSE_COVER.get('UPLOAD'), default=COURSE_COVER.get('DEFAULT'),
                              max_length=100, verbose_name='课程封面')
    tag = models.CharField(max_length=20, default='', verbose_name='课程标签')
    tips = models.CharField(max_length=300, default='', verbose_name='课程须知')
    tell_you = models.CharField(max_length=300, default='', verbose_name='老师告诉你')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    stu_nums = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.name, self.org.name)

    def get_lesson_nums(self):
        """
        章节数
        :return:
        """
        return self.lesson_set.count()

    def get_lessons(self):
        """
        获取所有章节
        :return:
        """
        return self.lesson_set.all()

    def get_learn_users(self):
        """
        获取学习用户
        :return:
        """
        return self.usercourse_set.all()[:5]


class CourseBanner(Course):
    """
    轮播课程
    后台管理有：1 课程管理 2 轮播课程管理
    不需要有数据表
    """
    class Meta:
        proxy = True    # 不会生成新表
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    """
    课程章节
    """
    course = models.ForeignKey(Course, verbose_name='所属课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.name, self.course.name)

    def get_videos(self):
        """
        获取所有视频
        :return:
        """
        return self.video_set.all()


class Video(models.Model):
    """
    章节视频
    """
    lesson = models.ForeignKey(Lesson, verbose_name='所属章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    url = models.URLField(max_length=200, default='', verbose_name='访问地址', unique=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    课程资源
    """
    COURSE_RESOURCE = COURSE_UPLOAD.get('RESOURCE')

    course = models.ForeignKey(Course, verbose_name='所属课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to=COURSE_RESOURCE.get('UPLOAD'), max_length=100, verbose_name='资源文件')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.name, self.course.name)





