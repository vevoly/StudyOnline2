from time import gmtime

from django.db import models

from user.models import UserProfile
from utils.choices import gender_choices, org_type_choices, org_recommend_choices
from StudyOnline2.settings import ORG_UPLOAD, TEACHER_UPLOAD


class CityDict(models.Model):
    """
    城市字典
    """
    name = models.CharField(max_length=20, unique=True, verbose_name='城市名')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Org(models.Model):
    """
    机构
    """
    ORG_LOGO = ORG_UPLOAD.get('LOGO')

    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    name = models.CharField(max_length=50, verbose_name='机构名')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(max_length=5, choices=org_type_choices, default=org_type_choices[0][0], verbose_name='机构类别')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    logo = models.ImageField(upload_to=ORG_LOGO.get('UPLOAD'), default=ORG_LOGO.get('DEFAULT'), verbose_name='机构Logo')
    tag = models.CharField(max_length=20, verbose_name='机构标签')
    recommend = models.SmallIntegerField(choices=org_recommend_choices, default=3, verbose_name='推荐指数')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏次数')
    stu_nums = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数量')
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'city', 'address')
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_classic_courses(self):
        """
        经典课程
        学习人数最多的3门课程
        :return:
        """
        return self.course_set.order_by('-stu_nums')[:3]

    def get_teacher_nums(self):
        """
        获取讲师数量
        :return:
        """
        return self.teacher_set.count()


class Teacher(models.Model):
    """
    讲师
    """
    TEACHER_AVATAR = TEACHER_UPLOAD.get('AVATAR')

    org = models.ForeignKey(Org, verbose_name='所属机构')
    name = models.CharField(max_length=10, verbose_name='讲师名')
    gender = models.CharField(choices=gender_choices, default=gender_choices[0][0], max_length=10, verbose_name='讲师性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    avatar = models.ImageField(upload_to=TEACHER_AVATAR.get('UPLOAD'), max_length=100, default=TEACHER_AVATAR.get('DEFAULT'), verbose_name='讲师头像')
    work_years = models.SmallIntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    teach_feature = models.CharField(max_length=100, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏次数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        unique_together = ('org', 'name', 'gender', 'birthday')
        verbose_name = '讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s (%s)' % (self.name, self.org.name)

    def get_age(self):
        """
        获取讲师年龄
        :return:
        """
        return gmtime().tm_year - self.birthday.year


