import os
import json
import pika


def produce(host, body):
    user = os.getenv("RABBITMQ_USER", os.getenv("RABBITMQ_DEFAULT_USER", "admin")).strip("'\" ")
    pwd = os.getenv("RABBITMQ_PASS", os.getenv("RABBITMQ_DEFAULT_PASS", "y90:SU28i{u@")).strip("'\" ")

    credentials = pika.PlainCredentials(user, pwd)
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs", durable=True)
    channel.queue_bind(
        queue="router_jobs", exchange="jobs", routing_key="check_interfaces"
    )

    # แปลงข้อมูลเป็น string หากถูกส่งมาเป็น dict/object
    if isinstance(body, (dict, list)):
        body = json.dumps(body)

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)
    connection.close()
