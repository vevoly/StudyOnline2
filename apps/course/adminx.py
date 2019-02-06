# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 1:39'

import xadmin

from .models import CourseCategory, Course, Lesson, Resource, Video, CourseBanner


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = Resource
    extra = 0


class CourseAdmin(object):
    """
    正常课程
    """
    list_display = ['name', 'desc', 'detail', 'level', 'learn_times', 'cover', 'stu_nums', 'fav_nums', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'level', 'stu_nums', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'level', 'learn_times', 'stu_nums', 'fav_nums', 'click_nums',
                   'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['stu_nums', 'fav_nums']
    exclude = ['click_nums']
    style_field = {'detail': 'ueditor'}
    model_icon = 'fa fa-book'

    inlines = [LessonInline, CourseResourceInline]


class CourseBannerAdmin(object):
    """
    轮播课程
    """
    list_display = ['name', 'desc', 'detail', 'level', 'learn_times', 'cover', 'stu_nums', 'fav_nums', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'level', 'stu_nums', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'level', 'learn_times', 'stu_nums', 'fav_nums', 'click_nums',
                   'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['stu_nums', 'fav_nums']
    exclude = ['click_nums']
    style_field = {'detail': 'ueditor'}
    model_icon = 'fa fa-tv'

    inlines = [LessonInline, CourseResourceInline]

    # 显示结果集
    def queryset(self):
        """
        只显示可以轮播的课程
        :return:
        """
        qs = super(CourseBannerAdmin, self). queryset()
        return qs.filter(is_banner=True)

    # 保存model
    def save_models(self):
        """
        保存课程的时候统计机构课程数,
        xadmin后台新增和修改都会走这里
        :return:
        """
        obj = self.new_obj
        obj.save()
        if obj.org is not None:
            obj.org.course_nums = Course.objects.filter(org=obj.org)
            obj.org.save()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-newspaper-o'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']
    model_icon = 'fa fa-file-video-o'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download', 'add_time']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file'


xadmin.site.register(CourseCategory)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseBanner, CourseBannerAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Resource, CourseResourceAdmin)

