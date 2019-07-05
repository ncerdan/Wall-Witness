""" Imports """
# Public
import datetime
import db_ops
#make update pr function and test with
#   boulder/tr to set to 6/12

db_ops.add_workout('bench', datetime.date(2019, 2, 12), 3, 8, 115, 125)
