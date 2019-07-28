""" Imports """
# Public
import datetime
import db_ops


start = datetime.datetime(2019, 7, 2)
end   = datetime.datetime(2019, 7, 27)
type  = 'Bwght'

x, y = db_ops.get_data_points(start, end, type)

my_x = []
my_y = y

for date in x:
    my_x.append(date.strftime('%m/%d/%Y'))

print(my_x)
print(my_y)
