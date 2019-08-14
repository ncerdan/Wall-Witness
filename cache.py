""" Import """
# Public
import datetime

# Personal
import constants

""" Class Definition """
class Cache():
    """
    * Internal storage data structures to implement:
                --------------------------

        date_range_cached = {ax_option : (datetime.datetime, datetime.datetime)}
            (None if not cached)
        data               = {ax_option : [(datetime.datetime, data_point)]}
         ^^ (will not check unless date_ranged_cached != None)
    """

    def __init__(self):
        # List of ax-options to cache
        self.data_options_list = [constants.marshalled_graph_ax_options[o] for o in constants.graph_ax_options_list if o != '--']
        self.date_range_cached = {key:(None, None) for key in self.data_options_list}
        self.data              = {key:None for key in self.data_options_list}

    # returns date range cached for a given ax-option
    def get_date_range_cached(self, ax_option):
        return self.date_range_cached.get(ax_option) # Note: get() returns None if bad

    # Sets date range cached for a given ax_option
    def set_date_range_cached(self, ax_option, start, end):
        self.date_range_cached[ax_option] = (start, end)

    def all_in_cache(self, ax_option, start_date, end_date):
        """
        Checks whether all needed data between dates is stored in cache.
        Args:
            ax_option  (string):            axis option in question
            start_date (datetime.datetime): start date of query
            end_date   (datetime.datetime): end date of query
        Returns:
            Boolean
        """

        # Get date range
        cache_start_date, cache_end_date = self.get_date_range_cached(ax_option)

        # Case for empty cache
        if cache_start_date == None and cache_end_date == None:
            return False

        # Return if query dates are included in cached dates
        return cache_start_date <= start_date and cache_end_date >= end_date

    def add_to_cache(self, ax_option, date_list, data_list):
        """
        Add data to cache. date_list and data_list must have same length
        Args:
            ax_option  (string):             axis option in question
            date_list ([datetime.datetime]): list of x-values in order
            data_list ([float]):             list of y-values in order
        Returns:
            Boolean - if successful.
        """

        # Check lengths are the same
        if len(date_list) != len(data_list):
            return False

        # Create list of tuples to add to cache and get min/max date
        list_of_tuples = []

        #assuming len > 0
        min_date = date_list[0]
        max_date = date_list[0]
        for i in range(len(date_list)):
            list_of_tuples.append((date_list[i], data_list[i]))

            if date_list[i] < min_date:         # NEED TO TEST FULLY
                min_date = date_list[i]         #
            if date_list[i] > max_date:         #
                max_date = date_list[i]         #

        # Assume this data is not already in the cache?
        #     will assume yes for now...

        # Either create value list with data or add to existing list
        current = self.data[ax_option]
        if current == None:
            self.data[ax_option] = list_of_tuples
        else:
            # sort where data goes so it remains in order?
            self.data[ax_option].append(list_of_tuples)

        # Update cache date range
        cache_start_date, cache_end_date = self.get_date_range_cached(ax_option)
        if cache_start_date == None and cache_end_date == None:
            self.set_date_range_cached(ax_option, min_date, max_date)
        else:
            if min_date < cache_start_date:
                new_start = min_date
            else:
                new_start = cache_start_date

            if max_date > cache_end_date:
                new_end = max_date
            else:
                new_ed = cache_end_date

            self.set_date_range_cached(ax_option, new_start, new_end)

        # Success
        return True

    def clear_cache(self, ax_option):
        """
        Removes ax_option's cached data and metadata.
        Args:
            ax_option (string): axis option in question
        Returns:
            null
        """

        # Removes its data
        self.data[ax_option] = None

        # Removes its date range
        self.date_range_cached[ax_option] = (None, None)
