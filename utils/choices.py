# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/26 0026 下午 9:42'

"""
性别选择
"""
gender_choices = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知'),
    )

"""
发送电子邮件验证码选择
"""
send_type_choices = (
        ('reg', '注册'),
        ('fgt', '找回密码'),
        ('upd', '修改邮箱'),
    )

"""
培训机构类型选择
"""
org_type_choices = (
        ('px', '培训机构'),
        ('gr', '个人'),
        ('gx', '高校'),
    )

"""
培训机构推荐指数
"""
org_recommend_choices = (
    (1, '☆'),
    (2, '☆☆'),
    (3, '☆☆☆'),
    (4, '☆☆☆☆'),
    (5, '☆☆☆☆☆'),
)

"""
课程级别选择
"""
course_level_choices = (
        ('primary', '初级'),
        ('middle', '中级'),
        ('advanced', '高级'),
    )

"""
收藏类型选择
"""
fav_type_choices = (
    (1, '课程'),
    (2, '机构'),
    (3, '讲师'),
)
