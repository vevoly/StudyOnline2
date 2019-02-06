# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 12:53'

import xadmin

from .models import CityDict, Org, Teacher


class CityAdmin(object):
    search_fields = ['name']
    list_filter = ['name', 'add_time']
    model_icon = 'fa fa-building'


class OrgAdmin(object):
    list_display = ['name', 'desc', 'logo', 'click_nums', 'fav_nums', 'city', 'address', 'course_nums',  'add_time']
    search_fields = ['name', 'desc', 'logo', 'city', 'address']
    list_filter = ['name', 'desc', 'logo', 'click_nums', 'fav_nums', 'city', 'address', 'add_time']
    readonly_fields = ['click_nums', 'fav_nums', 'course_nums', 'stu_nums']
    model_icon = 'fa fa-institution'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position',
                    'teach_feature', 'click_nums', 'fav_nums']
    search_fields = ['org__name', 'name', 'work_years', 'work_company', 'work_position',
                     'teach_feature']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position',
                    'teach_feature', 'click_nums', 'fav_nums', 'add_time']
    readonly_fields = ['click_nums', 'fav_nums']
    model_icon = 'fa fa-mortar-board'


xadmin.site.register(CityDict, CityAdmin)
xadmin.site.register(Org, OrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

