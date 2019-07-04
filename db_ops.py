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

""" Functions """
# Adding Documents
def add_session(type_s, envr_s, avGr_s, hiGr_s, date_s, durn_s, locn_s, note_s):
    """
    Insert new session data into the sessions collection
    * Params:
        type of workout [bench, neg, pistol]    (string)
        date for entry                          (datetime.date)
        sets of exercise                        (int)
        reps for ecah set of exercise           (float)
        weight average                          (float)
        weight maximum                          (float)
    * Return:
        none                                    (n/a)
    """

def add_workout(type, date, sets, reps, avWt, hiWt):
    """
    Insert new workout data into the workouts collection.
    Args:
        type (string): type of workout [bench, neg,  pistol],
        date (datetime.date): date for entry,
        sets (int): sets of exercise,
        reps (float): reps for each set of exercise,
        avWt (float): weight average,
        hiWt (float): weight maximum.
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
    workouts.insert_one(to_insert)

def add_weight(date, wght):
    """
    Insert new weight data into the weights collection.
    Args:
        date (datetime.date): date for entry,
        wght (float): weight for entry.
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
    weights.insert_one(to_insert)

# Updating Documents?

# Deleting Documents (how? -- based off of what?)
def del_session():
    return -999

def del_workout():
    return -999

def del_weight():
    return -999
