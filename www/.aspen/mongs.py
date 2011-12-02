import pymongo
from pymongo.objectid import ObjectId, InvalidId

def get_value(request):
    """Given a request object, return a value. Use for *.txt and *.json.
    """
    server = request.path['server']
    database = request.path['database']
    collection = request.path['collection']
    _id = request.path['filter']
    key = request.path['value'] # derp

    db = pymongo.Connection(server, slave_okay=True)[database][collection]

    try:
        _id = ObjectId(_id)
    except InvalidId:
        pass
    document = db.find_one(_id)
    return document[key]
