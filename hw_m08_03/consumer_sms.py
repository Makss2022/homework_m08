import sys
import pika

import connect
from models import Contacts

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sent_objectid', exchange_type='topic')
channel.queue_declare(queue='sms', durable=True)
channel.queue_bind(exchange='sent_objectid', queue='sms')
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_message_to_email(phone, name_contact):
    print(f"SMS sent to {name_contact} by phone: '{phone}'")


def callback(ch, method, properties, body: bytes):
    id_contact = body.decode()
    contact = Contacts.objects(pk=id_contact)
    send_message_to_email(contact[0].phone, contact[0].fullname)
    contact.update(message_sent=True)
    print(contact[0].message_sent)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='sms', on_message_callback=callback)


if __name__ == '__main__':
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
