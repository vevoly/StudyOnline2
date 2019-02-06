# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/28 0028 下午 9:44'

from django.conf.urls import url

from .views import OrgListView, OrgHomeView, AddUserAskView, CourseListView, OrgDescView, \
    TeacherListView, TeacherView, TeacherDetailView, AddFavView

urlpatterns = [
    # 机构列表页
    url(r'^$', OrgListView.as_view(), name='org_list'),
    # 机构主页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    # 咨询
    url(r'^ask/$', AddUserAskView.as_view(), name='add_ask'),
    # 机构课程
    url(r'^courses/(?P<org_id>\d+)/$', CourseListView.as_view(), name='org_course'),
    # 机构详情
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    # 机构教师
    url(r'^teacher/(?P<org_id>\d+)/$', TeacherView.as_view(), name='org_teacher'),
    # 收藏
    url(r'^fav/$', AddFavView.as_view(), name='add_fav')

]