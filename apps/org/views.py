from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse

from pure_pagination import Paginator, PageNotAnInteger

from .models import Org, CityDict
from course.models import Course, Teacher
from operation.models import UserFav
from utils.choices import org_type_choices
from utils.beans import OrgTypeBean
from utils.mixin_utils import LoginRequiredMixin
from .forms import AddUserAskForm


def has_faved(request, fav_type=1, fav_id=0):
    """
    是否已收藏
    :param request:
    :param fav_type: 1 课程；2 机构；3 教师
    :param fav_id:
    :return:
    """
    ret = False
    if request.user.is_authenticated():
        ret = UserFav.objects.filter(user=request.user, fav_type=fav_type, fav_id=fav_id).exists()
    return ret


class OrgListView(View):
    """
    机构列表
    """
    @staticmethod
    def get(request):
        # 所有机构
        all_orgs = Org.objects.all()
        # 授课机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:5]
        # 所有城市
        all_citys = CityDict.objects.all()
        # 所有机构类型
        all_types = list()
        for t in org_type_choices:
            all_types.append(OrgTypeBean(t[0], t[1]))
        # 搜索关键字
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
            search_type = 'org'
        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 筛选机构类别
        ct = request.GET.get('ct', '')
        if ct:
            all_orgs = all_orgs.filter(category=ct)
        # 机构总数
        org_nums = all_orgs.count()
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            all_orgs = all_orgs.order_by('-' + sort)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        all_orgs = p.page(page)

        return render(request, 'org/org-index.html', locals())


class OrgHomeView(View):
    """
    各机构首页
    """
    @staticmethod
    def get(request, org_id):
        current_page = 'home'
        course_org = Org.objects.all().get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = Course.objects.all().filter(org=course_org)[:3]
        all_teachers = Teacher.objects.all().filter(org=course_org)[:3]
        has_fav = has_faved(request, 2, int(org_id))  # 机构是否收藏
        return render(request, 'org/org-detail-homepage.html', locals())


class AddUserAskView(View):
    """
    用户咨询, ajax
    """
    @staticmethod
    def post(request):
        ask_form = AddUserAskForm(request.POST)
        ret = dict()
        if ask_form.is_valid():
            ask_form.save(commit=True)
            ret['status'] = 'success'
        else:
            ret['status'] = 'fail'
            # print(ask_form.errors['mobile'])
            if ask_form.has_error('name'):
                ret['message'] = '名字输入有错误！'
            elif ask_form.has_error('mobile'):
                ret['message'] = '手机格式输入有错误！'
            elif ask_form.has_error('course_name'):
                ret['message'] = '课程名输入有错误！'
        return JsonResponse(ret)


class CourseListView(View):
    """
    课程列表
    """
    @staticmethod
    def get(request, org_id):
        current_page = 'course'
        course_org = Org.objects.all().get(id=int(org_id))
        all_courses = Course.objects.all().filter(org_id=int(org_id))
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 5, request=request)
        all_courses = p.page(page)
        return render(request, 'org/org-list-course.html', locals())


class OrgDescView(View):
    """
    机构详情
    """
    @staticmethod
    def get(request, org_id):
        current_page = 'desc'
        course_org = Org.objects.get(id=int(org_id))
        has_fav = has_faved(request, 2, int(org_id))
        return render(request, 'org/org-detail-desc.html', locals())


class TeacherListView(View):
    """
    所有教师列表
    """
    @staticmethod
    def get(request):
        all_teachers = Teacher.objects.all()
        sorted_teacher = all_teachers.order_by('-click_nums')[:5]
        # 关键字
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teachers = all_teachers.filter(name__icontains=keywords)
            search_type = 'teacher'
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        all_teachers = p.page(page)
        return render(request, 'teacher/teachers-list.html', locals())


class TeacherView(View):
    """
    机构教师列表
    """
    @staticmethod
    def get(request, org_id):
        current_page = 'teacher'
        course_org = Org.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all().order_by('-click_nums')
        has_fav = has_faved(request, 2, int(org_id))  # 机构是否收藏
        return render(request, 'org/org-list-teachers.html', locals())


class TeacherDetailView(View):
    """
    教师详情
    """
    @staticmethod
    def get(request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        has_teacher_faved = has_faved(request, 3, int(teacher_id))  # 教师是否收藏
        has_org_faved = has_faved(request, 2, int(teacher.org_id))  # 机构是否收藏
        all_courses = Course.objects.all().filter(teacher=teacher)
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:5]
        teacher.click_nums += 1
        teacher.save()
        return render(request, 'teacher/teacher-detail.html', locals())


class AddFavView(LoginRequiredMixin, View):
    """
       添加收藏
    """
    def set_fav_nums(self, fav_type, fav_id, num=1):
        """
        添加/取消收藏更改相应的数量
        :param fav_type:
        :param fav_id:
        :param num:
        :return:
        """
        if fav_type == 1:
            course = Course.objects.get(id=fav_id)
            course.fav_nums += num
            course.save()
        elif fav_type == 2:
            org = Org.objects.get(id=fav_id)
            org.fav_nums += num
            org.save()
        elif fav_type == 3:
            teacher = Teacher.objects.get(id=fav_id)
            teacher.fav_nums += num
            teacher.save()

    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        ret = dict()
        # 检查是否已收藏
        if request.user.is_authenticated():
            recs = UserFav.objects.all().filter(fav_id=fav_id, fav_type=fav_type, user=request.user)
            if recs:    # 有的话，就删除收藏
                recs.delete()
                self.set_fav_nums(fav_type=fav_type, fav_id=fav_id, num=-1)
                ret['status'] = 'success'
                ret['msg'] = '收藏'
            else:   # 没有就添加收藏
                user_fav = UserFav()
                if fav_id and fav_type:
                    user_fav.user = request.user
                    user_fav.fav_type = fav_type
                    user_fav.fav_id = fav_id
                    user_fav.save()
                    self.set_fav_nums(fav_type, fav_id)
                    ret['status'] = 'success'
                    ret['msg'] = '已收藏'
        else:
            ret['status'] = 'fail'
            ret['msg'] = '用户未登录！'
        return JsonResponse(ret)
