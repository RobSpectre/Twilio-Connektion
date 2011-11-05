'''
Models
'''

from google.appengine.ext import db

class User(db.Model):
    AccountSid = db.StringProperty()
    From = db.StringProperty()
    phone_number = db.StringProperty()
    Body = db.StringProperty()
    City = db.StringProperty()
    State = db.StringProperty()
    Zip = db.StringProperty()
    Country = db.StringProperty()
    active = db.BooleanProperty(default=True)
    date = db.DateTimeProperty(auto_now_add=True)
    RecordingUrl = db.StringProperty()

class Connection(db.Model):
    CallSid = db.StringProperty()
    phone_number = db.StringProperty()
    From = db.StringProperty()
    To = db.StringProperty()
    Duration = db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)
