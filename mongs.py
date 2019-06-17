"""Helper functions for Mongs.
"""
import datetime
import math
import os
import json

import pymongo
from bson.objectid import ObjectId, InvalidId


def commaize(n, places=1):
    """Given a number, return a string with commas and a decimal -- 1,000.0.
    """
    out = ("%%.0%df" % places) % n
    try:
        whole, fraction = out.split('.')
    except ValueError:
        whole, fraction = (out, '')
    _whole = []
    for i, digit in enumerate(reversed(whole), start=1):
        _whole.insert(0, digit)
        if i % 3 == 0:
            _whole.insert(0, ',')
    out = ''.join(_whole + ['.', fraction]).lstrip(',').rstrip('.')
    return out


def get_single_document_filter(_id):
    filter = {"_id": {"$in": [_id]}}
    try:
        # Under some combination of MongoDB/PyMongo versions, this is
        # necessary.
        object_id = ObjectId(_id)
    except InvalidId:
        pass
    else:
        filter['_id']['$in'].append(object_id)
    return filter


def get_value(request):
    """Given a request object, return a value. Use for *.txt and *.json.
    """
    server = request.path['server']
    database = request.path['database']
    collection = request.path['collection']
    _id = request.path['filter']
    key = request.path['value']  # derp

    db = pymongo.MongoClient(server)[database][collection]
    filter = get_single_document_filter(_id)
    document = db.find_one(filter)
    return document[key]


def dt2age(dt):
    """Given a Unix timestamp (UTC) or a datetime object, return an age string
    relative to now.

        range                                       denomination    example
        ======================================================================
        0-1 second                                 "just a moment"
        1-59 seconds                                seconds         13 seconds
        60 sec - 59 min                             minutes         13 minutes
        60 min - 23 hrs, 59 min                     hours           13 hours
        24 hrs - 13 days, 23 hrs, 59 min            days            13 days
        14 days - 27 days, 23 hrs, 59 min           weeks           3 weeks
        28 days - 12 months, 31 days, 23 hrs, 59 mn months          6 months
        1 year -                                    years           1 year

    We'll go up to years for now.

    Times in the future are indicated by "in (denomination)" and times
    already passed are indicated by "(denomination) ago".

    """

    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.utcfromtimestamp(dt)

    # Define some helpful constants.
    # ==============================

    sec = 1
    min = 60 * sec
    hr = 60 * min
    day = 24 * hr
    wk = 7 * day
    mn = 4 * wk
    yr = 365 * day

    # Get the raw age in seconds.
    # ===========================

    now = datetime.datetime.utcnow()
    age = abs(now - dt).total_seconds()

    # Convert it to a string.
    # =======================
    # We start with the coarsest unit and filter
    # to the finest. Pluralization is centralized.

    if age < 1:
        return 'just a moment'

    elif age >= yr:         # years
        amount = age / yr
        unit = 'year'
    elif age >= mn:         # months
        amount = age / mn
        unit = 'month'
    elif age >= (2 * wk):   # weeks
        amount = age / wk
        unit = 'week'
    elif age >= day:        # days
        amount = age / day
        unit = 'day'
    elif age >= hr:         # hours
        amount = age / hr
        unit = 'hour'
    elif age >= min:        # minutes
        amount = age / min
        unit = 'minute'
    else:                   # seconds
        amount = age
        unit = 'second'

    # Pluralize and return.
    # =====================

    amount = int(math.floor(amount))
    if amount != 1:
        unit += 's'
    age = ' '.join([str(amount), unit])
    fmt = 'in {age}' if dt > now else '{age} ago'
    return fmt.format(age=age)


def has_documents(coll):
    """
    Return a boolean for the presence of documents in the collection.
    """
    return bool(coll.count())


def connect(server):
    """
    Allow SERVER_URIS to override the URI for a server.
    """
    full_uris = json.loads(os.environ.get('SERVER_URIS', '{}'))
    return pymongo.MongoClient(full_uris.get(server, server))
