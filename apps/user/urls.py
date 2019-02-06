# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/27 0027 下午 6:45'

from django.conf.urls import url

from .views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView,\
    UserAvatarView, UserPasswordView, UserEmailCodeView, UserEmailView, ForgetPwdView,\
    ResetPwdView, ModifyPwdView, UserMessageView, UserCourseView, UserFavCourseView, \
    UserFavOrgView, UserFavTeacherView#, DelFavView
from org.views import AddFavView


urlpatterns = [
    # 注册
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 激活
    url(r'^active/(?P<code>.*)/$', ActiveView.as_view(), name='active'),
    # 登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 登出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 忘记密码
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 重置密码
    url(r'^reset/(?P<code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    # 修改密码
    url(r'^resetpwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 个人中心-我的资料
    url(r'^center/$', UserInfoView.as_view(), name='center'),
    # 修改头像
    url(r'^update/avatar/$', UserAvatarView.as_view(), name='avatar'),
    # 修改密码
    url(r'^update/pwd/$', UserPasswordView.as_view(), name='pwd'),
    # 修改邮箱-获取邮件验证码
    url(r'^update/email/code/$', UserEmailCodeView.as_view(), name='update_email_code'),
    # 修改邮箱-修改邮箱
    url(r'^update/email/$', UserEmailView.as_view(), name='update_email'),
    # 我的消息
    url(r'^message/$', UserMessageView.as_view(), name='message'),
    # 我的收藏-课程
    url(r'^fav/course/$', UserFavCourseView.as_view(), name='fav_course'),
    # 我的收藏-讲师
    url(r'^fav/teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    # 我的收藏-机构
    url(r'^fav/org/$', UserFavOrgView.as_view(), name='fav_org'),
    # 删除收藏
    url(r'^fav/delete/$', AddFavView.as_view(), name='del_fav'),
    # 我的课程
    url(r'^course/$', UserCourseView.as_view(), name='course'),

]