from mongoengine import *


class Contacts(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField(max_length=30)
    send_method = StringField(max_length=5)
    message_sent = BooleanField(default=False)
