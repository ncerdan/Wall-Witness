######################
# Main Window values #
######################

# Axis options control
graph_ax_options_list = ['--',
                     'Boulder - Average Grade',
                     'Boulder - High Grade',
                     'Toprope - Average Grade',
                     'Toprope - High Grade',
                     'Sport - Average Grade',
                     'Sport - High Grade',
                     'Bench Press - Max Weight',
                     'Bench Press - Average Weight',
                     'Bench Press - Sets',
                     'Bench Press - Reps',
                     'One-Arm Negative - Max Weight',
                     'One-Arm Negative - Average Weight',
                     'One-Arm Negative - Sets',
                     'One-Arm Negative - Reps',
                     'Pistol Squat - Max Weight',
                     'Pistol Squat - Average Weight',
                     'Pistol Squat - Sets',
                     'Pistol Squat - Reps',
                     'Body Weight']

marshalled_graph_ax_options = {
    'Boulder - Average Grade':           'SBavGr',
    'Boulder - High Grade' :             'SBhiGr',
    'Toprope - Average Grade':           'STavGr',
    'Toprope - High Grade':              'SThiGr',
    'Sport - Average Grade':             'SSavGr',
    'Sport - High Grade':                'SShiGr',
    'Bench Press - Max Weight':          'WBhiWt',
    'Bench Press - Average Weight':      'WBavWt',
    'Bench Press - Sets':                'WBsets',
    'Bench Press - Reps':                'WBreps',
    'One-Arm Negative - Max Weight':     'WOhiWt',
    'One-Arm Negative - Average Weight': 'WOavWt',
    'One-Arm Negative - Sets':           'WOsets',
    'One-Arm Negative - Reps':           'WOreps',
    'Pistol Squat - Max Weight':         'WPhiWt',
    'Pistol Squat - Average Weight':     'WPavWt',
    'Pistol Squat - Sets':               'WPsets',
    'Pistol Squat - Reps':               'WPreps',
    'Body Weight':                       'BWwght'
}

# Dialog control
SESSION = 0
WORKOUT = 1
WEIGHT  = 2

# Plotting control
CLEAR_BOTH   = 0
CLEAR_LEFT   = 1
CLEAR_RIGHT  = 2
UPDATE_LEFT  = 3
UPDATE_RIGHT = 4

# Granularity control
DAILY      = 0
WEEKLY     = 1
BIWEEKLY   = 2
MONTHLY    = 3
BIMONTHLY  = 4
SIXMONTHLY = 5
YEARLY     = 6

#########################
# Session Dialog Values #
#########################
session_types_ist = ['--', 'Boulder', 'Top-Rope', 'Sport']
marshalled_session_types = {
    'Boulder': 'boulder',
    'Top-Rope': 'toprope',
    'Sport': 'sport'
}

session_envr_list  = ['--', 'Indoors', 'Outdoors']
marshalled_session_envr = {
    'Indoors': 'in',
    'Outdoors': 'out'
}

time_units_list = ['hr', 'min']

bldr_grade_list  = ['--', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
rope_grade_list  = ['--', '5.9', '5.10a', '5.10b', '5.10c', '5.10d', '5.11a', '5.11b', '5.11c', '5.11d',
                                 '5.12a', '5.12b', '5.12c', '5.12d', '5.13a', '5.13b', '5.13c', '5.13d']
marshalled_grades = {
    # Bouldering grade mappings
    'V0': 0, 'V1': 1, 'V2': 2,  'V3': 3,   'V4': 4,   'V5': 5,   'V6': 6,
    'V7': 7, 'V8': 8, 'V9': 9, 'V10': 10, 'V11': 11, 'V12': 12, 'V13': 13,

    # Rope grade mappings
      '5.9': 9.00,
    '5.10a': 10.00, '5.10b': 10.25, '5.10c': 10.50, '5.10d': 10.75,
    '5.11a': 11.00, '5.11b': 11.25, '5.11c': 11.50, '5.11d': 11.75,
    '5.12a': 12.00, '5.12b': 12.25, '5.12c': 12.50, '5.12d': 12.75,
    '5.13a': 13.00, '5.13b': 13.25, '5.13c': 13.50, '5.13d': 13.75
}

##########################
# Workout Dialogs Values #
##########################
workout_types_list = ['--', 'Bench Press', '1-Arm Negative', 'Pistol Squat']
marshalled_workout_types = {
    'Bench Press': 'bench',
    '1-Arm Negative': 'neg',
    'Pistol Squat': 'pistol'
}

########################
# Weight Dailog Values #
########################
weight_units_list = ['lbs', 'kg']

#######################
# DBOps Object Values #
#######################
NO_CACHE = 0
ALL_IN_CACHE = 1
LATER_THAN_CACHE = 2
EARLIER_THAN_CACHE = 3
SURROUND_CACHE = 4

"""   TESTING   """
def get_status_text(status):
    if status == NO_CACHE:
        return "nothing in cache"
    elif status == ALL_IN_CACHE:
        return "all in cache"
    elif status == LATER_THAN_CACHE:
        return "later than cache"
    elif status == EARLIER_THAN_CACHE:
        return "earlier than cache"
    elif status == SURROUND_CACHE:
        return "surrounding cache"
    else:
        return "undefined status input"
""" END TESTING """
