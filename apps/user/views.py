from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import transaction

from pure_pagination import Paginator

from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserMessage, UserCourse, UserFav
from course.models import Course, Teacher
from org.models import Org
from .forms import RegisterForm, LoginForm, UserInfoForm, UpdateAvatarForm, \
    UpdatePasswordForm, UpdateEmailCodeForm, UpdateEmailForm, ForgetPwdForm
from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    """
    重写ModelBackend中的authenticate，以达到可以使用邮箱或手机号登录
    """
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserProfile.objects.get(Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            UserModel().set_password(password)


class RegisterView(View):
    """
    用户注册
    """
    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    @staticmethod
    @transaction.atomic()
    def post(request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            # email是否存在
            email_exist = UserProfile.objects.filter(email=email)
            if email_exist:
                return render(request, 'register.html', {'msg': '邮箱已经存在，请更换邮箱。'})
            # 1 保存 2 发送激活邮件 3 写入欢迎注册消息
            user = UserProfile()
            user.email = email
            user.username = email
            user.password = make_password(password)
            user.is_active = 0
            user.save()
            send_email(email)
            welcome = UserMessage()
            welcome.user = user
            welcome.message = '欢迎注册在线学校网'
            welcome.save()
            return render(request, 'send_success.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    """
    用户激活
    """
    @staticmethod
    def get(request, code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for rec in all_records:
                email = rec.email
                user = UserProfile.objects.get(email=email)
                if user.is_active == 0:
                    user.is_active = 1
                    user.save()
                    return redirect('account:login')
        else:
            return render(request, 'active_fail.html')


class LoginView(View):
    """
    用户登录
    """
    @staticmethod
    def get(request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    @staticmethod
    def post(request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', '')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('index')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """
    退出登录
    """
    @staticmethod
    def get(request):
        logout(request)
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('index')


class ForgetPwdView(View):
    """
    忘记密码
    """
    @staticmethod
    def get(request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    @staticmethod
    def post(request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            # 发送邮件
            send_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    """
    重置密码
    """
    @staticmethod
    def get(request, code):
        # 验证code是否存在
        all_records = EmailVerifyRecord.objects.filter(code=code, send_type='forget')
        if all_records:
            for rec in all_records:
                email = rec.email
                return render(request, 'resetpwd.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    """
    修改密码
    """
    @staticmethod
    def post(request):
        email = request.POST.get('email', '')
        modify_form = UpdatePasswordForm(request.POST)
        if modify_form.is_valid():
            password = modify_form.cleaned_data['password2']
            users = UserProfile.objects.filter(email=email)
            if users.count() == 0:
                return render(request, 'resetpwd.html', {"msg": "会员不存在！"})
            else:
                user = users[0]
                user.password = make_password(password)
                user.save()
                return redirect('account:login')
        else:
            return render(request, 'resetpwd.html', {'modify_form': modify_form, 'email': email})


class UserInfoView(View):
    """
    用户中心
    """
    @staticmethod
    @login_required(login_url='/account/login/')
    def get(request):
        return render(request, 'usercenter/usercenter-info.html')

    @staticmethod
    @login_required(login_url='/account/login/')
    def post(request):
        info_form = UserInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(info_form.errors)


class UserAvatarView(LoginRequiredMixin, View):
    """
    修改头像
    """
    @staticmethod
    def post(request):
        avatar_form = UpdateAvatarForm(request.POST, request.FILES, instance=request.user)
        ret = dict()
        if avatar_form.is_valid():
            # avatar = avatar_form.cleaned_data['avatar']
            avatar_form.save()
            ret['status'] = 'success'
        else:
            ret['status'] = 'fail'
        return JsonResponse(ret)


class UserPasswordView(LoginRequiredMixin, View):
    """
    修改密码
    """
    @staticmethod
    def post(request):
        pwd_form = UpdatePasswordForm(request.POST)
        ret = dict()
        if pwd_form.is_valid():
            password = pwd_form.cleaned_data['password2']
            request.user.password = make_password(password)
            request.user.save()
            ret['status'] = 'success'
        else:
            ret['status'] = 'fail'
            ret['msg'] = '修改密码失败！'
        return JsonResponse(ret)


class UserEmailCodeView(LoginRequiredMixin, View):
    """
    发送修改邮箱验证码
    """
    @staticmethod
    def get(request):
        email_code_form = UpdateEmailCodeForm(request.GET)
        ret = dict()
        if email_code_form.is_valid():
            email = email_code_form.cleaned_data['email']
            # 判断邮箱是否存在
            if UserProfile.objects.filter(email=email):
                ret['status'] = 'fail'
                ret['msg'] = '邮箱已存在！'
            else:
                # 发送验证码
                send_email(email, 'upd_email')
                ret['status'] = 'success'
        else:
            ret['status'] = 'fail'
            ret['msg'] = '邮箱格式输入有误！'
        return JsonResponse(ret)


class UserEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """
    @staticmethod
    def post(request):
        email_form = UpdateEmailForm(request.POST)
        ret = dict()
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            ret['status'] = 'success'
        else:
            ret['status'] = 'fail'
            ret['msg'] = '验证码有错误'

        return JsonResponse(ret)


class UserMessageView(LoginRequiredMixin, View):
    """
    用户消息
    """
    @staticmethod
    def get(request):
        all_messages = UserMessage.objects.filter(user=request.user)
        all_unread_messages = all_messages.filter(is_read=0)
        for unread_message in all_unread_messages:
            unread_message.is_read = 1
            unread_message.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 6, request=request)
        messages = p.page(page)
        return render(request, 'usercenter/usercenter-message.html', {"messages": messages})


class UserCourseView(LoginRequiredMixin, View):
    """
    用户课程
    """
    @staticmethod
    def get(request):
        user_course_list = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter/usercenter-mycourse.html', locals())


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏-课程
    """
    @staticmethod
    def get(request):
        course_ids = get_fav_ids(request.user)
        course_list = Course.objects.filter(id__in=course_ids)
        return render(request, 'usercenter/usercenter-fav-course.html', {'course_list': course_list})


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏-机构
    """
    @staticmethod
    def get(request):
        org_ids = get_fav_ids(request.user, 2)
        org_list = Org.objects.filter(id__in=org_ids)
        return render(request, 'usercenter/usercenter-fav-org.html', {'org_list': org_list})


class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户收藏-讲师
    """
    @staticmethod
    def get(request):
        teacher_ids = get_fav_ids(request.user, 3)
        teacher_list = Teacher.objects.filter(id__in=teacher_ids)
        return render(request, 'usercenter/usercenter-fav-teacher.html', {'teacher_list': teacher_list})


def get_fav_ids(user, fav_type=1):
    """
    获取收藏id
    :param user:
    :param fav_type:
    :return:
    """
    ret = []
    fav_list = UserFav.objects.filter(user=user, fav_type=fav_type)
    if fav_list:
        ret = [fav.fav_id for fav in fav_list]
    return ret


class IndexView(View):
    """
    主页
    """
    @staticmethod
    def get(request):
        # 获取主页轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:5]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = Org.objects.all()[:15]
        return render(request, 'index.html', locals())


