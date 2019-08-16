""" Imports """
# Public
import datetime
from cache import Cache


c = Cache()

date_list1 = [datetime.datetime(2019, 1, 2), datetime.datetime(2019, 1, 3), datetime.datetime(2019, 1, 4)]
data_list1 = [2, 3, 4]

date_list2 = [datetime.datetime(2019, 1, 5), datetime.datetime(2019, 1, 6)]
data_list2 = [5, 6]

c.add_one_range_to_cache('Bwght', date_list2, data_list2)
print(c.data)
print(c.get_date_range_cached('Bwght'))

c.add_one_range_to_cache('Bwght', date_list1, data_list1)

print(c.data)
print(c.get_date_range_cached('Bwght'))

c.clear_cache('Bwght')

print(c.data)
print(c.get_date_range_cached('Bwght'))

""" ----------------------------------------------------- """

c.add_one_range_to_cache('Bwght', date_list1, data_list1)
print(c.data)
print(c.get_date_range_cached('Bwght'))

c.add_one_range_to_cache('Bwght', date_list2, data_list2)

print(c.data)
print(c.get_date_range_cached('Bwght'))

c.clear_cache('Bwght')

print(c.data)
print(c.get_date_range_cached('Bwght'))
