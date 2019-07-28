""" Imports """
# Public
from pymongo import MongoClient
import datetime

""" Setup """
# Connecting to MongoDB Atlas
client = MongoClient("mongodb://ncerdan:AzsiRNGAC6dMdsqe@ncerdan-shard-00-00-bqvu0.mongodb.net:27017,ncerdan-shard-00-01-bqvu0.mongodb.net:27017,ncerdan-shard-00-02-bqvu0.mongodb.net:27017/test?ssl=true&replicaSet=ncerdan-shard-0&authSource=admin&retryWrites=true&w=majority")

# Connecting to Database
db = client.get_database('wallwitness_db')

# Getting Collections
sessions = db.sessions
workouts = db.workouts
weights  = db.weights
prs      = db.prs

""" Functions """
# Adding Documents
def add_session(type, envr, avGr, hiGr, date, durn, locn, note):
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
        none.
    """

    #marshalling data
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

    #insert it
    sessions.insert_one(to_insert)

    #check if it is a new pr
    check_new_pr(type_i, hiGr_i, date)

def add_workout(type, date, sets, reps, avWt, hiWt):
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
        none.
    """

    #marshalling data
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

    #insert it
    workouts.insert_one(to_insert)

    #check if it is a new pr
    check_new_pr(type_i, hiWt_i, date)

def add_weight(date, wght):
    """
    Insert new weight data into the weights collection.
    Args:
        date (datetime.datetime): date for entry,
        wght (float):             weight for entry.
    Returns:
        none.
    """

    #marshalling data
    date_i = date
    wght_i = float(wght)
    to_insert = {
        'date': date_i,
        'wght': wght_i
    }

    #insert it
    weights.insert_one(to_insert)

    #check if it is a new pr
    check_new_pr('wght', wght_i, date)

# Updating Documents
def check_new_pr(type, new_data, date):
    """
    Checks if new entry sets a new pr, and if it does updates it.
    Args:
        type (string):            type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'wght'],
        new_data (float):         new grade/weight pr,
        date (datetime.datetime): date of new pr.
    Returns:
        none.
    """

    #get the current pr record of the given type
    curr_pr = prs.find_one({'type': type})
    curr_rd = curr_pr['rcrd']

    #compare it to the new weight/grade
    if new_data > curr_rd:
        upd_pr(type, new_data, date)

def upd_pr(type, rcrd, date):
    """
    Updates correct pr with new date and record.
    Args:
        type (string):            type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol', 'weight'],
        rcrd (float):             new grade/weight pr,
        date (datetime.datetime): date pr was attained.
    Returns:
        none.
    """

    #marshalling data
    date_i = date
    to_update = {
        'type': type,
        'rcrd': rcrd,
        'date': date_i
    }

    #update the correct pr's to the new data
    prs.update({'type': type}, to_update)

# Deleting Documents (based off of what?)
def del_session():
    return -999

def del_workout():
    return -999

def del_weight():
    return -999

# Querying Data
def get_data_points(start, end, desired):
    """
    Gets type data between start and end dates.
    Args:
        start (datetime.datetime): earliest date to query from
        end (datetime.datetime):   latest date to query from
        desired (string):          what data to query ['SBhiGr', 'SBavGr', 'SThiGr', 'STavGr', 'SShiGr', 'SSavGr',
                                                       'WBhiWt', 'WBavWt', 'WBsets', 'WBreps', 'WOhiWt', 'WOavWt',
                                                       'WOsets', 'WOreps', 'WPhiWt', 'WPavWt', 'WPsets', 'WPreps',
                                                       'Bwght']  =  (wall_witness. marshalled_data.values())
    Returns:
        ([datetime.datetime], [float]) for graphing
    """
    # Session query
    if desired[0] == 'S':
        col = sessions
        if desired[1] == 'B':
            type = 'boulder'
        elif desired[1] == 'T':
            type = 'toprope'
        else:
            type = 'sport'

        cursor = col.find({
            'date': {'$gte': start, '$lte': end},
            'type': {'$eq': type}
        })
        key = desired[2:]

    # Workout query
    elif desired[0] == 'W':
        col = workouts
        if desired[1] == 'B':
            type = 'bench'
        elif desired[1] == 'O':
            type = 'neg'
        else:
            type = 'pistol'

        cursor = col.find({
            'date': {'$gte': start, '$lte': end},
            'type': {'$eq': type}
        })
        key = desired[2:]

    # Bodyweight query
    else:
        col = weights
        cursor = col.find({ 'date': { '$gte': start, '$lte': end }})
        key = 'wght'

    # Create tuple of lists to return
    x = []
    y = []
    for doc in cursor:
        date = doc['date']
        data = doc[key]
        x.append(date)
        y.append(data)

    return x, y
