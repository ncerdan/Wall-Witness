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
        Predicate for whether all needed data between dates is stored in cache.
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

    def add_data_to_cache(self, ax_option, date_list, data_list, range_start, range_end):
        """
        Add data from one continuous range to cache (data is disjoint from what in cache already).
        Args:
            ax_option  (string):             axis option in question    [constants.marshalled_graph_ax_options.values()]
            date_list ([datetime.datetime]): list of x-values in order
            data_list ([float]):             list of y-values in order
            range_start (datetime.datetime): inclusive date start of range covered by data
            range_end   (datetime.datetime): inclusize date end of range convered by data
        Returns:
            Boolean - if successful.
        """

        # Check lengths are the same and positive
        if len(date_list) != len(data_list) or len(date_list) < 1:
            print("Bad input to add_data_to_cache")
            return False

        # Create list of tuples to add to cache
        list_of_tuples = []

        for i in range(len(date_list)):
            list_of_tuples.append((date_list[i], data_list[i]))

        # Assume this data is not already in the cache?
        #     will assume yes for now...

        # Either create new data list or add to existing list. Update date range accordingly
        current = self.data[ax_option]
        cache_start_date, cache_end_date = self.get_date_range_cached(ax_option)
        if current == None:
            self.data[ax_option] = list_of_tuples
            self.set_date_range_cached(ax_option, range_start, range_end)
        else:
            # Place new data either at start or end of cached data
            #    since assuming this data is disjoint with new data
            #    AND new data must be bordering cached data

            # New data before cache data
            if range_end < cache_start_date:
                list_of_tuples.extend(self.data[ax_option])
                self.data[ax_option] = list_of_tuples
                self.set_date_range_cached(ax_option, range_start, cache_end_date)
            # New data after cache data
            elif range_start > cache_end_date:
                self.data[ax_option].extend(list_of_tuples)
                self.set_date_range_cached(ax_option, cache_start_date, range_end)

        # Success
        return True

    def query_data_from_cache(self, ax_option, start, end):
        """
        Queries data from cache for option ax_option from start to end inclusive.
        Args:
            ax_option (string): axis option to query for [constants.marshalled_graph_ax_options.values()]
            start (datetime.datetime): inclusive start date for query
            end   (datetime.datetime): inclusive end date for query
        Returns:
            ([datetime.datetime], [float])
        """

        # Get list in data structure
        list = self.data[ax_option]
        if list == None:
            print('cache query error')
            return

        # Create the two lists to return by splitting up cached tuples
        date_list = []
        data_list = []
        for (date, data) in list:
            # Make sure data is within query limits
            if start <= date and date <= end:
                date_list.append(date)
                data_list.append(data)

        # Return result
        return (date_list, data_list)

    def clear_cache_by_type(self, type):
        """
        Removes all cached data and metadata related to type.
        Args:
            type (string): type of axis option to remove ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'wght']
        Returns:
            Boolean - if succeeded
        """

        if type == 'boulder':
            # Remove bouldering data
            self.clear_cache_by_ax_option('SBavGr')
            self.clear_cache_by_ax_option('SBhiGr')
        elif type == 'toprope':
            # Remove toprope data
            self.clear_cache_by_ax_option('STavGr')
            self.clear_cache_by_ax_option('SThiGr')
        elif type == 'sport':
            # Remove sport data
            self.clear_cache_by_ax_option('SSavGr')
            self.clear_cache_by_ax_option('SShiGr')
        elif type == 'bench':
            # Remove bench-press data
            self.clear_cache_by_ax_option('WBhiWt')
            self.clear_cache_by_ax_option('WBavWt')
            self.clear_cache_by_ax_option('WBsets')
            self.clear_cache_by_ax_option('WBreps')
        elif type == 'neg':
            # Remove 1-arm negative data
            self.clear_cache_by_ax_option('WOhiWt')
            self.clear_cache_by_ax_option('WOavWt')
            self.clear_cache_by_ax_option('WOsets')
            self.clear_cache_by_ax_option('WOreps')
        elif type == 'pistol':
            # Remove pistol squat data
            self.clear_cache_by_ax_option('WPhiWt')
            self.clear_cache_by_ax_option('WPavWt')
            self.clear_cache_by_ax_option('WPsets')
            self.clear_cache_by_ax_option('WPreps')
        elif type == 'wght':
            # remove body weight data
            self.clear_cache_by_ax_option('BWwght')
        else:
            # Error handle bad input
            print(type + " is not valid input to clear_cache_by_type.")
            return False

        return True

    def clear_cache_by_ax_option(self, ax_option):
        """
        Removes ax_option's data and metadata.
        Args:
            type (ax_option): axis option to remove [constants.marshalled_graph_ax_options.values()]
        Returns:
            null
        """

        # Removes its data
        self.data[ax_option] = None

        # Removes its date range
        self.date_range_cached[ax_option] = (None, None)

    def print(self, ax_opt=None):
        if ax_opt != None:
            print('=====================================')
            print(ax_opt + ':')
            print('-----')
            print('Data:')
            print(self.data[ax_opt])
            print('Date Range:')
            print(self.get_date_range_cached(ax_opt))
        else:
            for ax_option in constants.marshalled_graph_ax_options.values():
                print('=====================================')
                print(ax_option + ':')
                print('-----')
                print('Data:')
                print(self.data[ax_option])
                print('Date Range:')
                print(self.get_date_range_cached(ax_option))
