import pika
import os
import time
from callback import callback

def main():
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    user = os.getenv("RABBITMQ_USER", "admin")
    password = os.getenv("RABBITMQ_PASS", "rabbitmq")

    creds = pika.PlainCredentials(user, password)
    
    # วนลูปพยายามเชื่อมต่อ RabbitMQ (Retry Logic)
    for i in range(10):
        try:
            print(f"Connecting to RabbitMQ (try {i})...")
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=host, credentials=creds)
            )
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(3)
    else:
        print("Could not connect to RabbitMQ")
        return

    ch = conn.channel()
    
    # ประกาศ Queue ให้ตรงกับ Scheduler (ต้องใส่ durable=True)
    ch.queue_declare(queue="router_jobs", durable=True)

    # ตั้งค่าให้ RabbitMQ ส่งงานให้ Worker ทีละ 1 งาน (กระจายงานแบบ Fair Dispatch)
    ch.basic_qos(prefetch_count=1)

    # ผูกฟังก์ชัน callback เพื่อรับงานจาก queue
    ch.basic_consume(
        queue="router_jobs", 
        on_message_callback=callback, 
        auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    ch.start_consuming()

if __name__ == "__main__":
    main()
