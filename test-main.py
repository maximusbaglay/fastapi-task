broker = RabbitBroker("127.0.0.1/data_queue")
stream = FastStream(broker)

# RabbitMQ

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue="data_queue")

async def process_message(message):
    print(f"Получено сообщение: {message.body}")
    try:
        data = json.loads(message.body)
        query = f"INSERT INTO data (key, value) VALUES ('{data['key']}', '{data['value']}')"
        clickhouse_connection.execute(query)
    except Exception as e:
        print(f"Error processing message: {str(e)}")

# ClickHouse

clickhouse_connection = ClickHouseClient.connect(
    host="127.0.0.1",
    port=8000,
    database="default",
    user="default",
    password="default"
)
@router.post("/send")
async def send_data(data: dict):
    try:
        serialized_data = json.dumps(data)
        rabbitmq_channel.basic_publish(exchange="", routing_key="data_queue", body=serialized_data)
        return {"message": "Сообщение передано успешно"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data")
async def get_data():    
    try:
        query = "SELECT * FROM data"
        result = clickhouse_connection.execute(query)
        data = [{"key": row[0], "value": row[1]} for row in result]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_data() -> dict:
    try:
        query = "SELECT * FROM data"
        result = clickhouse_connection.execute(query)
        data = [{"key": row[0], "value": row[1]} for row in result]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue', durable=True)
channel.basic_publish(exchange='', routing_key='my_queue', body='Hello, RabbitMQ!')
print(" [x] Sent 'Hello, RabbitMQ!'")

connection.close()

import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue', durable=True)

channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

from faststream import FastStream
from faststream.rabbit import RabbitBroker
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)

@broker.subscriber("test-queue")  # название очереди RMQasync 
def handle(msg: str):    
	print(msg)
 
 @router.get("/data")
 async def get_data():
    clickhouse_connection = ClickHouseClient.connect(
        host="127.0.0.1",
        port=8123,
        database="moex",
        user="default",
        password="default"
    )
    query = "SELECT * FROM data"
    result = clickhouse_connection.execute(query)
    data = [{"key": row[0], "value": row[1]} for row in result]
    return {"data": data}