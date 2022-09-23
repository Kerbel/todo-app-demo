import json
import logging

from kafka import KafkaConsumer
from twilio.rest import Client

consumer = KafkaConsumer(
    'todo_updates',
    bootstrap_servers='kafka:9092',
    api_version=(0, 11, 5),
    value_deserializer=lambda m: m.decode('utf-8')
)

TWILIO_ACCOUNT_SID = "ACeaaf7b4abf2629bff30d3c87befe05b0"
TWILIO_AUTH_TOKEN = "afa38d018b1a9460db59dc73809d2101"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms(action_type: str):
    body_message = "New todo item added to your list"
    if action_type == 'delete':
        body_message = "Todo item deleted from your list"

    print(f"Sending SMS with the following content: {body_message}")

    sms_message = client.messages \
        .create(
        body=body_message,
        from_='+15005550006',
        to='+972547332522'
    )

    print(sms_message.sid)


def handle_kafka_message(message):
    kafka_message = message.value
    try:
        print(f"receive message id: {kafka_message}")
        send_sms(kafka_message)
    except Exception as e:
        print("excpetion on 'handle_kafka_messgae")
        print(e)


for message in consumer:
    handle_kafka_message(message)
