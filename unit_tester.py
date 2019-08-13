""" Imports """
# Public
import datetime
import cache


c = cache.Cache()

print(c.data_options_list)
print(c.date_ranged_cached)

print(c.get_date_range_cached('bad'))
print(c.get_date_range_cached('Bwght'))
