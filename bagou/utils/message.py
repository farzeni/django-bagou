# -*- coding: utf-8 -*-
import json
import pika

from django.conf import settings


def __send(message):
    cred = pika.PlainCredentials(
        settings.BAGOU.get('AMQP_BROKER_USER'),
        settings.BAGOU.get('AMQP_BROKER_PASS'))

    param = pika.ConnectionParameters(
        host=settings.BAGOU.get('AMQP_BROKER_ADDR'),
        port=settings.BAGOU.get('AMQP_BROKER_PORT'),
        virtual_host=settings.BAGOU.get('AMQP_BROKER_PATH'),
        credentials=cred)

    body = json.dumps(message)

    conn = pika.BlockingConnection(param)
    channel = conn.channel()
    channel.basic_publish(
        exchange='', routing_key=settings.BAGOU.get('QUEUE_NAME'), body=body)


def broadcast(channel, event, data={}, callback=None):
    """
    Broadcast message to channel(s).

    channel     (str)(list) : Channel(s) to send message.
    event       (str)       : Message event type.
    data        (dict)      : Data to be attached in message.
    callback    (str)       : Callback to be send in message.
    """
    if not isinstance(channel, list):
        channel = [channel]

    data = {'event': event, 'callbackId': callback, 'channel': channel, 'data': data}
    __send(data)
