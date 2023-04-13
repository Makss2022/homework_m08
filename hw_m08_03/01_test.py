import pika
import faker

import connect
from models import Contacts

fake = faker.Faker('uk-UA')

for el in range(6):
    contact = Contacts(fullname=fake.name())
    contact.email = fake.email()
    contact.phone = fake.phone_number()
    contact.send_method = "sms" if el < 3 else "email"
    contact.save()

    message = str(contact.id)
    routing_key = contact.send_method
    print(contact.phone)
    print(routing_key, type(routing_key))
