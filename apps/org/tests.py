from django.test import TestCase

from utils.choices import org_type_choices
from utils.beans import OrgTypeBean

from time import gmtime

# all_types = list()
# for t in org_type_choices:
#     print(t[0], '-', t[1])
#     all_types.append(OrgTypeBean(t[0], t[1]))
#
# # print(all_types)
#
# for t in all_types:
#     print(t.id, ':-> ', t.name)

print(gmtime().tm_year - 1984)