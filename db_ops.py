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
prs = db.prs

""" Functions """
# Adding Documents
def add_session(type, envr, avGr, hiGr, date, durn, locn, note):
    """
    Insert new session data into the sessions collection.
    For rope climbing grades: a=.00,b=.25,c=.50,d=.75
    Args:
        type (string):        type of climbing ['boulder', 'toprope', 'sport'],
        envr (string):        environment ['in', 'out'],
        avGr (float):         average grade of session,
        hiGr (float):         highest grade of session,
        date (datetime.date): date for entry,
        durn (float):         length of session,
        locn (string):        location of session,
        note (string):        notes of session.
    Returns:
        none.
    """
    #marshalling data
    type_i = str(type)
    envr_i = str(envr)
    avGr_i = float(avGr)
    hiGr_i = float(hiGr)
    date_i = date.strftime("%Y-%m-%d")
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
        type (string):        type of workout ['bench', 'neg',  'pistol'],
        date (datetime.date): date for entry,
        sets (int):           sets of exercise,
        reps (float):         reps for each set of exercise,
        avWt (float):         weight average,
        hiWt (float):         weight maximum.
    Returns:
        none.
    """
    #marshalling data
    type_i = str(type)
    date_i = date.strftime("%Y-%m-%d")
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
        date (datetime.date): date for entry,
        wght (float):         weight for entry.
    Returns:
        none.
    """
    #marshalling data
    date_i = date.strftime("%Y-%m-%d")
    wght_i = float(wght)
    to_insert = {
        'date': date_i,
        'wght': wght_i
    }

    #insert it
    weights.insert_one(to_insert)

# Updating Documents
def check_new_pr(type, new_data, date):
    """
    Checks if new entry sets a new pr, and if it does updates it.
    Args:
        type (string):        type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol'],
        new_data (float):     new grade/weight pr,
        date (datetime.date): date of new pr.
    Returns:
        none.
    """

    #check if type is bad?

    #get the current pr of the given type
    curr_pr = prs.find_one({'type': type})
    curr_rd = curr_pr['rcrd']

    #compare it to the new weight/grade
    if new_data > curr_rd:
        upd_pr(type, new_data, date)

def upd_pr(type, rcrd, date):
    """
    Updates correct pr with new date and record.
    Args:
        type (string):        type of pr ['boulder', 'toprope', 'sport', 'bench', 'neg', 'pistol'],
        rcrd (float):         new grade/weight pr,
        date (datetime.date): date pr was attained.
    Returns:
        none.
    """
    #marshalling data
    date_i = date.strftime("%Y-%m-%d")
    to_update = {
        'type': type,
        'rcrd': rcrd,
        'date': date_i
    }

    #update the correct pr's to the new data
    prs.update({'type': type}, to_update)

# Deleting Documents (how? -- based off of what?)
def del_session():
    return -999

def del_workout():
    return -999

def del_weight():
    return -999
