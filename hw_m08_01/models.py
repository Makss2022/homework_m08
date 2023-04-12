from mongoengine import *


class Authors(Document):
    fullname = StringField(max_length=50)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField()


class Qoutes(Document):
    quote = StringField()
    author = ReferenceField(Authors)
    tags = ListField(StringField(max_length=50))
