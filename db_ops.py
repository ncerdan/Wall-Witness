""" Imports """
# Public
from pymongo import MongoClient
from datetime import datetime, timedelta

# Personal
from cache import Cache
import constants
import private

""" Variables  """
url = private.url

class DBOps():
    """ Setup """
    def __init__(self):
        # Connecting to MongoDB Atlas and connecting to Database
        self.client = MongoClient(url)
        self.db = self.client.get_database('wallwitness_db')

        # Getting Collections
        self.sessions = self.db.sessions
        self.workouts = self.db.workouts
        self.weights  = self.db.weights
        self.prs      = self.db.prs

        # Initializing cache
        self.cache = Cache()

    """ Functions """
    # Adding Documents
    def add_session(self, type, envr, avGr, hiGr, date, durn, locn, note):
        """
        Insert new session data into the sessions collection.
        For rope climbing grades: a=.00,b=.25,c=.50,d=.75
        Args:
            type (string):            type of climbing ['boulder', 'toprope', 'sport'],
            envr (string):            environment ['in', 'out'],
            avGr (float):             average grade of session,
            hiGr (float):             highest grade of session,
            date (datetime.datetime): date for entry,
            durn (float):             length of session,
            locn (string):            location of session,
            note (string):            notes of session.
        Returns:
            no return.
        """

        # Marshall data
        type_i = str(type)
        envr_i = str(envr)
        avGr_i = float(avGr)
        hiGr_i = float(hiGr)
        date_i = date
        durn_i = float(durn)
        locn_i = str(locn)
        note_i = str(note)
        to_insert = {
            'type': type_i,
            'envr': envr_i,
            'avGr': avGr_i,
            'hiGr': hiGr_i,
            'date': date_i,
            'durn': durn_i,
            'locn': locn_i,
            'note': note_i
        }

        # Insert it
        self.sessions.insert_one(to_insert)

        # Check if it is a new pr
        self.check_new_pr(type_i, hiGr_i, date)

        # Clear relevant cache data that is now dirty
        self.cache.clear_cache_by_type(type_i)

    def add_workout(self, type, date, sets, reps, avWt, hiWt):
        """
        Insert new workout data into the workouts collection.
        Args:
            type (string):            type of workout ['bench', 'neg',  'pistol'],
            date (datetime.datetime): date for entry,
            sets (int):               sets of exercise,
            reps (float):             reps for each set of exercise,
            avWt (float):             weight average,
            hiWt (float):             weight maximum.
        Returns:
            no return.
        """

        # Marshall data
        type_i = str(type)
        date_i = date
        sets_i = int(sets)
        reps_i = float(reps)
        avWt_i = float(avWt)
        hiWt_i = float(hiWt)
        to_insert = {
            'type': type_i,
            'date': date_i,
            'sets': sets_i,
            'reps': reps_i,
            'avWt': avWt_i,
            'hiWt': hiWt_i
        }

        # Insert it
        self.workouts.insert_one(to_insert)

        # Check if it is a new pr
        self.check_new_pr(type_i, hiWt_i, date)

        # Clear relevant cache data that is now dirty
        self.cache.clear_cache_by_type(type_i)

    def add_weight(self, date, wght):
        """
        Insert new weight data into the weights collection.
        Args:
            date (datetime.datetime): date for entry,
            wght (float):             weight for entry.
        Returns:
            no return.
        """

        # Marshall data
        date_i = date
        wght_i = float(wght)
        to_insert = {
            'date': date_i,
            'wght': wght_i
        }

        # Insert it
        self.weights.insert_one(to_insert)

        # Check if it is a new pr
        self.check_new_pr('wght', wght_i, date)

        # Clear relevant cache data that is now dirty
        self.cache.clear_cache_by_type('wght')

    # Updating Documents
    def check_new_pr(self, type, new_data, date):
        """
        Checks if new entry sets a new pr, and if it does updates it.
        Args:
            type (string):            type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'wght'],
            new_data (float):         new grade/weight pr,
            date (datetime.datetime): date of new pr.
        Returns:
            no return.
        """

        # Get the current pr record of the given type
        curr_pr = self.prs.find_one({'type': type})
        curr_rd = curr_pr['rcrd']

        # Compare it to the new weight/grade
        if new_data > curr_rd:
            self.update_pr(type, new_data, date)

    def update_pr(self, type, rcrd, date):
        """
        Updates correct pr with new date and record.
        Args:
            type (string):            type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'weight'],
            rcrd (float):             new grade/weight pr,
            date (datetime.datetime): date pr was attained.
        Returns:
            no return.
        """

        # Marshall data
        date_i = date
        to_update = {
            'type': type,
            'rcrd': rcrd,
            'date': date_i
        }

        # Update the correct pr to the new data
        self.prs.update({'type': type}, to_update)

    # Deleting Documents (based off of what?)
    def del_session(self):
        return -999

    def del_workout(self):
        return -999

    def del_weight(self):
        return -999

    # Querying Data
    def get_data_points(self, start, end, ax_option):
        """
        Gets type data between start and end dates.
        Args:
            start (datetime.datetime): earliest date to query from,
            end (datetime.datetime):   latest date to query from,
            ax_option (string):        axis option to query [constants.marshalled_graph_ax_options.values()].
        Returns:
            ([datetime.datetime], [float]) for graphing.
        """

        # Check to use cache, then only query what's needed
        cache_start, cache_end = self.cache.get_date_range_cached(ax_option)

        # If new query is not adjacent to cached data, clear the cache
        if (cache_end != None and cache_end < start) or (cache_start != None and end < cache_start):
            self.cache.clear_cache_by_ax_option(ax_option)

        if cache_start == None and cache_end == None:
            # No cached data
            db_query_start = start
            db_query_end   = end
            status         = constants.NO_CACHE
        elif cache_start <= start and cache_end >= end:
            # All needed data is cached
            c_query_start = start
            c_query_end   = end
            status        = constants.ALL_IN_CACHE
        elif cache_start <= start and cache_end < end:
            # Need to query 'later' than cache
            c_query_start  = start
            c_query_end    = cache_end
            db_query_start = cache_end + timedelta(days=1)
            db_query_end   = end
            status         = constants.LATER_THAN_CACHE
        elif cache_start > start and cache_end >= end:
            # Need to query 'earlier' than cache
            db_query_start = start
            db_query_end   = cache_start - timedelta(days=1)
            c_query_start  = cache_start
            c_query_end    = end
            status         = constants.EARLIER_THAN_CACHE
        elif cache_start > start and cache_end < end:
            # Need to query both 'earlier' and 'later' than cache
            left_db_query_start  = start
            left_db_query_end    = cache_start - timedelta(days=1)
            c_query_start        = cache_start
            c_query_end          = cache_end
            right_db_query_start = cache_end + timedelta(days=1)
            right_db_query_end   = end
            status               = constants.SURROUND_CACHE

        # Perform query specific by ax_option
        if ax_option[:2] == 'SB':
            col = self.sessions
            type = 'boulder'
        elif ax_option[:2] == 'ST':
            col = self.sessions
            type = 'toprope'
        elif ax_option[:2] == 'SS':
            col = self.sessions
            type = 'sport'
        elif ax_option[:2] == 'WB':
            col = self.workouts
            type = 'bench'
        elif ax_option[:2] == 'WO':
            col = self.workouts
            type = 'neg'
        elif ax_option[:2] == 'WP':
            col = self.workouts
            type = 'pistol'
        else:
            col = self.weights
            type = None

        # Key for type of data to query
        key = ax_option[2:]

        # Case where one database query is needed
        if status == constants.NO_CACHE or status == constants.EARLIER_THAN_CACHE or status == constants.LATER_THAN_CACHE:
            # Session or workout
            if type != None:
                cursor = col.find({
                    'date': {'$gte': db_query_start, '$lte': db_query_end},
                    'type': {'$eq': type}
                })
            # Body weight
            else:
                cursor = col.find({ 'date': { '$gte': db_query_start, '$lte': db_query_end }})

            # Format results
            db_x, db_y = self.parse_cursor(cursor, key)

            # Add new data to cache
            self.cache.add_data_to_cache(ax_option, db_x, db_y, db_query_start, db_query_end)

        # Case where two database queries are needed
        elif status == constants.SURROUND_CACHE:
            # Session or workout
            if type != None:
                left_cursor = col.find({
                    'date': {'$gte': left_db_query_start, '$lte': left_db_query_end},
                    'type': {'$eq': type}
                })
                right_cursor = col.find({
                    'date': {'$gte': right_db_query_start, '$lte': right_db_query_end},
                    'type': {'$eq': type}
                })
            # Body weight
            else:
                left_cursor  = col.find({ 'date': { '$gte': left_db_query_start, '$lte': left_db_query_end }})
                right_cursor = col.find({ 'date': { '$gte': right_db_query_start, '$lte': right_db_query_end }})

            # Format results
            l_db_x, l_db_y = self.parse_cursor(left_cursor, key)
            r_db_x, r_db_y = self.parse_cursor(right_cursor, key)

            # Add new data to cache
            self.cache.add_data_to_cache(ax_option, l_db_x, l_db_y, left_db_query_start, left_db_query_end)
            self.cache.add_data_to_cache(ax_option, r_db_x, r_db_y, right_db_query_start, right_db_query_end)

        # Now that everything is cached, get all data from the cache quickly (O(N))
        final_x, final_y = self.cache.query_data_from_cache(ax_option, start, end)

        # Return final result
        return final_x, final_y

    def parse_cursor(self, cursor, key):
        """
        Gets data from cursor using key and returns tuple of lists.
        Args:
            cursor (Cursor): cursor to results from db query,
            key (string):    four-character key for what data to get.
        Returns:
            ([datetime.datetime], [float]) for caching and graphing.
        """

        # Create list of tuples to sort
        list_of_tuples = []
        for doc in cursor:
            date = doc['date']
            data = doc[key]
            list_of_tuples.append((date, data))

        # Sort list based on date element in tuples
        sorted_list = sorted(list_of_tuples, key=lambda tup: tup[0])

        # Split into lists to return
        date_list = []
        data_list = []
        for (date, data) in sorted_list:
            date_list.append(date)
            data_list.append(data)

        return date_list, data_list
