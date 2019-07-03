# python3 file

#imports
from pymongo  import MongoClient
import datetime

#connecting to database
client = MongoClient("mongodb://ncerdan:AzsiRNGAC6dMdsqe@ncerdan-shard-00-00-bqvu0.mongodb.net:27017,ncerdan-shard-00-01-bqvu0.mongodb.net:27017,ncerdan-shard-00-02-bqvu0.mongodb.net:27017/test?ssl=true&replicaSet=ncerdan-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.get_database('wallwitness_db')

sessions = db.sessions_c
workouts = db.workouts_c
weights  = db.weights_c

# TESTING
test_to_add_to_weights = {
    'wght': 139.8,
    'date': datetime.date(2019, 7, 1).strftime("%Y-%m-%d")
}

weights.insert_one(test_to_add_to_weights)
