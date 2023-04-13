
import pika
import faker

import connect
from models import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sent_objectid', exchange_type='topic')
channel.queue_declare(queue='sms', durable=True)
channel.queue_declare(queue='email', durable=True)
channel.queue_bind(exchange='sent_objectid', queue='email')
channel.queue_bind(exchange='sent_objectid', queue='sms')


def main():
    fake = faker.Faker('uk-UA')

    for el in range(6):
        contact = Contacts(fullname=fake.name())
        contact.email = fake.email()
        contact.phone = fake.phone_number()
        contact.send_method = "sms" if el < 3 else "email"
        contact.save()

        message = str(contact.id)
        routing_key = contact.send_method

        channel.basic_publish(
            exchange='sent_objectid',
            routing_key=routing_key,
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main()
