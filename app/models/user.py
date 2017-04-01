import datetime
from flask import current_app
from mongoengine import *

class User(Document):
    fb_id = StringField(required=True)
    date_modified = DateTimeField(default=datetime.datetime.now)