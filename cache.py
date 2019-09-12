""" Import """
# Public
import datetime

# Personal
import constants

""" Class Definition """
class Cache():
    """
    * Internal storage data structures:
         --------------------------

        date_range_cached = {ax_option : (datetime.datetime, datetime.datetime)} (maps to (None, None) if not cached)
        data              = {ax_option : [(datetime.datetime, data_point)]}      (maps to None if not cached)

        * ax_option = [constants.marshalled_graph_ax_options.values()]
    """

    def __init__(self):
        # List of axis options to cache
        self.data_options_list = [constants.marshalled_graph_ax_options[o] for o in constants.graph_ax_options_list if o != '--']

        # Hash table that maps axis option to the date ranged currently cached for it
        self.date_range_cached = {key:(None, None) for key in self.data_options_list}

        # Hash table that maps axis option to the list of data points currently cached for it
        self.data              = {key:None for key in self.data_options_list}

    def get_date_range_cached(self, ax_option):
        """
        Gets the date range cached for a given axis option.
        Args:
            ax_option (string): axis option in question     [constants.marshalled_graph_ax_options.values()].
        Returns:
            (datetime.datetime, datetime.datetime) or (None, None) if cache is empty.
        """

        return self.date_range_cached.get(ax_option)

    # Sets date range cached for a given ax_option
    def set_date_range_cached(self, ax_option, start, end):
        """
        Sets the date range cached for a given axis option.
        Args:
            ax_option (string):        axis option in question     [constants.marshalled_graph_ax_options.values()],
            start (datetime.datetime): start date to set cache to,
            end   (datetime.datetime): end date to set cache to.
        Returns:
            no return.
        """

        self.date_range_cached[ax_option] = (start, end)

    def add_data_to_cache(self, ax_option, date_list, data_list, range_start, range_end):
        """
        Add one continuous range of data to the cache (data is disjoint from what in cached already).
        Args:
            ax_option   (string):              axis option in question    [constants.marshalled_graph_ax_options.values()],
            date_list   ([datetime.datetime]): list of x-values in order,
            data_list   ([float]):             list of y-values in order,
            range_start (datetime.datetime):   inclusive date start of range covered by data,
            range_end   (datetime.datetime):   inclusize date end of range convered by data.
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
            #    AND new data must be adjacent to cached data

            # New data goes before cache data
            if range_end < cache_start_date:
                list_of_tuples.extend(self.data[ax_option]) # change to list_of_tuples.extend(current) to be more efficient?
                self.data[ax_option] = list_of_tuples
                self.set_date_range_cached(ax_option, range_start, cache_end_date)
            # New data goes after cache data
            elif range_start > cache_end_date:
                self.data[ax_option].extend(list_of_tuples)
                self.set_date_range_cached(ax_option, cache_start_date, range_end)

        # Success
        return True

    def query_data_from_cache(self, ax_option, start, end):
        """
        Queries data from cache for ax_option from start to end inclusive.
        Args:
            ax_option (string):            axis option to query for [constants.marshalled_graph_ax_options.values()],
            start     (datetime.datetime): inclusive start date for query,
            end       (datetime.datetime): inclusive end date for query.
        Returns:
            ([datetime.datetime], [float]) or (None, None) if error.
        """

        # Get list in data structure
        list = self.data[ax_option]
        if list == None:
            print('cache querying empty list error')
            return (None, None)

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
            type (string): type of axis option to remove ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'wght'].
        Returns:
            Boolean - if succeeded.
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

        # Success
        return True

    def clear_cache_by_ax_option(self, ax_option):
        """
        Removes ax_option's data and metadata.
        Args:
            type (ax_option): axis option to remove [constants.marshalled_graph_ax_options.values()].
        Returns:
            no return.
        """

        # Remove its data
        self.data[ax_option] = None

        # Remove its metadata
        self.date_range_cached[ax_option] = (None, None)
