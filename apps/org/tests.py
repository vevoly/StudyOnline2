from django.test import TestCase
from django.db.models import F, Count

from time import gmtime

from utils.choices import org_type_choices
from utils.beans import OrgTypeBean
from org.models import Org, CityDict



# all_types = list()
# for t in org_type_choices:
#     print(t[0], '-', t[1])
#     all_types.append(OrgTypeBean(t[0], t[1]))
#
# # print(all_types)
#
# for t in all_types:
#     print(t.id, ':-> ', t.name)

# print(gmtime().tm_year - 1984)


class OrgTest(TestCase):

    def setUp(self):
        city = CityDict.objects.create(name='上海')
        Org.objects.bulk_create(
            [
                Org(name='zanneti', click_nums=2, fav_nums=10, city=city),
                Org(name='wangjiu', click_nums=10, fav_nums=0, city=city),
            ]
        )

    def test1(self):
        """
        收藏数大于点击数的讲师数量。
        :return:
        """

        expect_org = Org.objects.get(pk=1)
        expect_org_nums = 1
        actual_org_set = Org.objects.filter(fav_nums__gt=F('click_nums'))
        actual_org = actual_org_set[0]
        actual_org_nums = actual_org_set.count()
        self.assertEqual(expect_org_nums, actual_org_nums)
        self.assertEquals(expect_org, actual_org)

    def test2(self):
        pass

