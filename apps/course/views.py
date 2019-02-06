from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import JsonResponse

from pure_pagination import PageNotAnInteger, Paginator

from .models import Course, Resource, Video
from operation.models import UserCourse, Comment
from org.views import has_faved
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    """
    课程列表
    """
    @staticmethod
    def get(request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-click_nums')[:5]
        # 关键字
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))
            search_type = 'course'
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            all_courses = all_courses.order_by('-' + sort)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 5, request=request)
        all_courses = p.page(page)
        return render(request, 'course/course-list.html', locals())


class CourseDetailView(View):
    """
    课程详情
    """
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        relate_courses = Course.objects.filter(Q(tag=course.tag), ~Q(id=int(course_id)))[:2]
        has_fav_course = has_faved(request, 1, course_id)
        has_fav_org = has_faved(request, 2, course.org_id)
        course.click_nums += 1
        course.save()
        return render(request, 'course/course-detail.html', locals())


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    必须登录
    """
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = Resource.objects.filter(course=course).all()
        # 查找是否有学习记录
        if not exist_learned_record(course, request.user):
            add_learned_record(course, request.user)
        # 学过该课程的同学还学过什么
        relate_courses = learned_other_courses(course, request.user)
        return render(request, 'course/course-video.html', {
            "course": course,
            "all_resources": all_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论
    """
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = Comment.objects.filter(course=course).order_by('-add_time')
        all_resources = Resource.objects.filter(course=course).all()
        relate_courses = learned_other_courses(course, request.user)
        return render(request, 'course/course-comment.html', locals())

    @staticmethod
    def post(request):
        """
        添加评论
        :param request:
        :return:
        """
        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')
        ret = dict()
        if course_id == 0:
            ret['status'] = 'fail'
            ret['msg'] = '评论出错'
            return JsonResponse(ret)
        if not comments.strip():
            ret['status'] = 'fail'
            ret['msg'] = '请输入评论内容'
            return JsonResponse(ret)
        if not request.user.is_authenticated():
            ret['status'] = 'fail'
            ret['msg'] = '用户未登录'
            return JsonResponse(ret)
        course = Course.objects.get(id=course_id)
        course_comment = Comment()
        course_comment.course = course
        course_comment.user = request.user
        course_comment.comment = comments
        course_comment.save()
        ret['status'] = 'success'
        ret['msg'] = '评论成功！'
        return JsonResponse(ret)

class CourseVideoView(LoginRequiredMixin, View):
    """
    播放视频
    """
    @staticmethod
    def get(request, video_id):
        vedio = Video.objects.get(id=video_id)
        course = vedio.lesson.course
        if not exist_learned_record(course, request.user):
            add_learned_record(course, request.user)
        all_resources = Resource.objects.filter(course=course).all()
        relate_courses = learned_other_courses(course, request.user)
        return render(request, 'course/course-play.html', locals())


def exist_learned_record(course, user):
    """
    是否有学习记录
    :param course:
    :param user:
    :return:
    """
    if UserCourse.objects.filter(user=user, course=course).exists():
        return True
    else:
        return False


def add_learned_record(course, user):
    """
    增加学习记录
    :param course:
    :param user:
    :return:
    """
    user_course = UserCourse()
    user_course.user = user
    user_course.course = course
    user_course.save()
    course.stu_nums += 1
    course.save()


def learned_other_courses(course, user, nums=5):
    """
    学过该课程的学生还学过其它什么课程
    :param course: 课程
    :param user: 当前用户
    :param nums: 返回课程数量
    :return:
    """
    ret = []
    # 找出有多少学生学习过该课程，除了自己
    user_course_list = UserCourse.objects.filter(Q(course=course), ~Q(user=user))
    if user_course_list:
        # 找出学过该课程的学生id集合
        user_ids = [user_course.user_id for user_course in user_course_list]
        # 找出学过该课程学生还学习过其他课程
        user_course_list = UserCourse.objects.filter(Q(user_id__in=user_ids), ~Q(course=course))
        # 取出课程
        ret = [user_course.course for user_course in user_course_list][:nums]
    return ret