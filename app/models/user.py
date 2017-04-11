import datetime
from mongoengine import *

class User(Document):
    fb_id = StringField(required=True, unique=True)
    state = StringField(required=True)
    name = StringField()
    date_modified = DateTimeField(default=datetime.datetime.now)
    address = DictField()
    attempt_counter = IntField()
