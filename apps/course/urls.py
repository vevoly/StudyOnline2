# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/28 0028 下午 9:44'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, \
    CourseCommentView, CourseVideoView

urlpatterns = [
    # 课程列表页
    url(r'^$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^commment/$', CourseCommentView.as_view(), name='add_comment'),
    # 课程视频
    url(r'^video/(?P<video_id>\d+)/$', CourseVideoView.as_view(), name='video_play'),

]