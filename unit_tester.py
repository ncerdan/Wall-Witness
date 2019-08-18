""" Imports """
# Public
import datetime
from cache import Cache


c = Cache()

date_list1 = [datetime.datetime(2019, 1, 2), datetime.datetime(2019, 1, 3), datetime.datetime(2019, 1, 4)]
data_list1 = [200, 300, 400]

date_list2 = [datetime.datetime(2019, 1, 5), datetime.datetime(2019, 1, 6)]
data_list2 = [500, 600]

print('about to add data to Bwght:')
c.add_data_to_cache('Bwght', date_list1, data_list1)
print(c.data)
print('Bwght range: ' + str(c.get_date_range_cached('Bwght')))

print('about to add data to Bwght:')
c.add_data_to_cache('Bwght', date_list2, data_list2)
print(c.data)
print('Bwght range: ' + str(c.get_date_range_cached('Bwght')))


""" ----------------------------------------------------- """
date_list3 = [datetime.datetime(2018, 11, 18), datetime.datetime(2018, 12, 6), datetime.datetime(2018, 12, 31)]
data_list3 = [5.5, 6.3, 6.9]

date_list4 = [datetime.datetime(2018, 9, 1), datetime.datetime(2018, 10, 1), datetime.datetime(2018, 11, 1)]
data_list4 = [3.5, 4.5, 5.5]

print('about to add data to SBavGr:')
c.add_data_to_cache('SBavGr', date_list3, data_list3)
print(c.data)
print('SBavGr range: ' + str(c.get_date_range_cached('SBavGr')))

print('about to add data to SBhiGr:')
c.add_data_to_cache('SBhiGr', date_list4, data_list4)
print(c.data)
print('SBhiGr range: ' + str(c.get_date_range_cached('SBhiGr')))


""" ----------------------------------------------------- """

print('about to clear wght: ')
c.clear_cache_by_type('wght')
c.print('Bwght')

print('about to clear boulder: ')
c.clear_cache_by_type('boulder')
c.print()

print('')
c.print()
