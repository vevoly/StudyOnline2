# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 2:41'

import xadmin

from .models import UserAsk, UserFav, UserMessage, Comment, UserCourse


class UserAskAdmin:
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-handshake-o'


class CourseCommentsAdmin:
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user__username', 'course__name', 'comment', 'add_time']
    model_icon = 'fa fa-commenting-o'


class UserFavAdmin:
    list_display = ['user', 'fav_type', 'fav_id', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-star-o'


class UserMessageAdmin:
    list_display = ['user', 'message', 'is_read', 'add_time']
    search_fields = ['user', 'message', 'is_read']
    list_filter = ['user', 'message', 'is_read', 'add_time']
    model_icon = 'fa fa-volume-up'


class UserCourseAdmin:
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course__name', 'add_time']
    model_icon = 'fa fa-soccer-ball-o'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Comment, CourseCommentsAdmin)
xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
