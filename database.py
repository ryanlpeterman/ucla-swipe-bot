from tinydb import TinyDB, Query
from util import log

db = TinyDB('db.json')

def reset_db():
    """ deletes all records in the database """
    db.purge()

def get_user_obj(uid):
    """
    Given the id of a user, returns the dict corresponding to their record
    """
    q = Query()
    res = db.search(q.id == uid)

    if not res:
        res = [{'id': uid}]

    return res[0]

def update_user_obj(obj):
    """
    Given a dict in the correct format, updates the uid
    """
    uid = obj['id']
    q = Query()

    # if user doesnt currently exist
    if not db.update(obj, q.id == uid):
        db.insert(obj)

    return True

def is_user_complete(uid):
    """
    Returns True if user is complete/ready to be matched on
    """
    usr = get_user_obj(uid)

    return "where" in usr and "when" in usr and "is_buyer" in usr

def set_buyer(uid, is_buyer):
    """
    Given uid and if they are a buyer of seller, sets the users buying status
    """
    user = get_user_obj(uid)
    user["is_buyer"] = is_buyer
    update_user_obj(user)
    log("USER: {id} was set to {buyer}".format(id=uid, buyer=is_buyer))

def add_hall(uid, hall):
    """ adds given hall to list of halls for user given by uid """
    user = get_user_obj(uid)

    # if locations are set and this halls currently not added
    if "where" in user and hall not in user["where"]:
        user["where"].append(hall)

    # no locations set yet
    else:
        user["where"] = [hall]

    update_user_obj(user)
    log("Added location {hall} to user {id}".format(hall=hall, id=uid))

def add_time(uid, hour):
    """ adds given hour to list of hours for user given by uid """
    user = get_user_obj(uid)

    # if times are set and this time isn't currently inside db
    if "when" in user and hour not in user["when"]:
        user["when"].append(hour)

    # no locations set yet
    else:
        user["when"] = [hour]

    update_user_obj(user)
    log("Added time {hour} to user {id}".format(hour=hour, id=uid))
