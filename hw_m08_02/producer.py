
import pika
import faker

import connect
from models import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='messages_sent', exchange_type='direct')
channel.queue_declare(queue='messages', durable=True)
channel.queue_bind(exchange='messages_sent', queue='messages')


def main():
    fake = faker.Faker('uk-UA')

    for _ in range(5):
        contact = Contacts(fullname=fake.name())
        contact.email = fake.email()
        contact.save()

        message = str(contact.id)

        channel.basic_publish(
            exchange='messages_sent',
            routing_key='messages',
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    connection.close()


if __name__ == '__main__':
    main()
