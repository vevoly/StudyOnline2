# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2019/1/28 0028 下午 10:51'


class OrgTypeBean:
    """
    机构类型Bean
    用于往前端传递
    """
    id = ''
    name = ''

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return '{0}:{1}'.format(self.id, self.name)
