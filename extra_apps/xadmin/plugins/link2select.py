# _*_ coding: utf-8 _*_
import xadmin

__author__ = 'jevoly'
__date__ = '2018/12/14 0014 下午 2:52'

from xadmin.views import BaseAdminPlugin
from xadmin.views.edit import CreateAdminView, UpdateAdminView


class Link2Select(BaseAdminPlugin):
    """
    自定义二级联动插件
    默认不加载，只在需要加载的options中设置为True才加载
    """
    is_execute = False

    def init_request(self, *args, **kwargs):
        return bool(self.is_execute)

    def get_media(self, media):
        # 加入我们自己的js文件
        return media + self.vendor('xadmin.self.link2select.js')


xadmin.site.register_plugin(Link2Select, CreateAdminView)
xadmin.site.register_plugin(Link2Select, UpdateAdminView)



