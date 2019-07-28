""" Imports """
# Public
import datetime
import db_ops


start = datetime.datetime(2019, 7, 10)
end   = datetime.datetime(2019, 7, 27)

x, y = db_ops.get_data_points(start, end, 'SBavGr')

print(x)
print(y)
