"""StudyOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
# from django.contrib import admin

import xadmin

from org.views import TeacherListView, TeacherDetailView
from user.views import IndexView
from StudyOnline2.settings import MEDIA_ROOT#, STATIC_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    # 配置上传文件的处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 配置静态文件目录
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # 富文本路径
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^account/', include('user.urls', namespace='account')),
    url(r'^org/', include('org.urls', namespace='org')),
    url(r'^course/', include('course.urls', namespace='course')),
    # 所有教师列表
    url(r'^teacher/$', TeacherListView.as_view(), name='teacher_list'),
    # 教师详情
    url(r'^teacher/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
