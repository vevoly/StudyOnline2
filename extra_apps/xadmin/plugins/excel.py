# _*_ coding: utf-8 _*_
from xadmin.views import BaseAdminPlugin
from django.template import loader

__author__ = 'jevoly'
__date__ = '2018/12/13 0013 下午 1:29'



class ListImportExcelPlugin(BaseAdminPlugin):
    """
    自定义导入Excel插件
    """
    import_excel = False

    def init_request(self, *args, **kwargs):
        """
        确定是否加载插件
        :param args:
        :param kwargs:
        :return:
        """
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        """
        将自己的html文件显示到某个地方
        :param context:
        :param nodes:
        :return:
        """
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_))
