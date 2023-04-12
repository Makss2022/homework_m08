from mongoengine import *


class Contacts(Document):
    fullname = StringField()
    email = StringField()
    message_sent = BooleanField(default=False)
