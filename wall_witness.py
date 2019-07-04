# Note: write files in python3

""" Imports """
# Public
import datetime

# Private
import db_ops

""" TESTING """
db_ops.add_workout('neg', datetime.date(2019, 7, 2), 2, 1, 0, 0)
db_ops.add_workout('bench', datetime.date(2019, 7, 4), 3, 8, 115, 125)

