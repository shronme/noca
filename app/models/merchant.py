import datetime
from mongoengine import *

class Merchant(Document):
    merchant_id = StringField(required=True, unique=True)
    
    name = StringField()
    date_modified = DateTimeField(default=datetime.datetime.now)
    
