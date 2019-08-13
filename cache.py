""" Import """
# Public
import datetime

# Personal
import constants

""" Class Definition """
class Cache():
    """
    * Internal storage data structures to implement

        date_range_cached = {ax_option : (datetime.datetime, datetime.datetime)}
            (None if not cached)
        data               = {ax_option : [(datetime.datetime, data_point)]}
            (will not check unless date_ranged_cached != None)
    """

    def __init__(self):
        # List of ax-options to cache
        self.data_options_list = [constants.marshalled_graph_ax_options[o] for o in constants.graph_ax_options_list if o != '--']
        self.date_range_cached = {key:None for key in self.data_options_list}

    # returns date range cached for a given ax-option
    def get_date_range_cached(self, ax_option):
        # returns None if bad
        return self.date_range_cached.get(ax_option)

    #def get_data(self);
