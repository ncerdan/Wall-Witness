""" Imports """
# Public
import datetime
import db_ops


start = datetime.datetime(2019, 7, 5)
end   = datetime.datetime(2019, 7, 22)

db_ops.get_data_points(start, end, 'hiGr')
