# broker = RabbitBroker("127.0.0.1/data_queue")
# stream = FastStream(broker)

# # RabbitMQ

# rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
# rabbitmq_channel = rabbitmq_connection.channel()
# rabbitmq_channel.queue_declare(queue="data_queue")

# async def process_message(message):
#     print(f"Получено сообщение: {message.body}")
#     try:
#         data = json.loads(message.body)
#         query = f"INSERT INTO data (key, value) VALUES ('{data['key']}', '{data['value']}')"
#         clickhouse_connection.execute(query)
#     except Exception as e:
#         print(f"Error processing message: {str(e)}")

# # ClickHouse

# clickhouse_connection = ClickHouseClient.connect(
#     host="127.0.0.1",
#     port=8000,
#     database="default",
#     user="default",
#     password="default"
# )
# @router.post("/send")
# async def send_data(data: dict):
#     try:
#         serialized_data = json.dumps(data)
#         rabbitmq_channel.basic_publish(exchange="", routing_key="data_queue", body=serialized_data)
#         return {"message": "Сообщение передано успешно"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/data")
# async def get_data():    
#     try:
#         query = "SELECT * FROM data"
#         result = clickhouse_connection.execute(query)
#         data = [{"key": row[0], "value": row[1]} for row in result]
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# async def get_data() -> dict:
#     try:
#         query = "SELECT * FROM data"
#         result = clickhouse_connection.execute(query)
#         data = [{"key": row[0], "value": row[1]} for row in result]
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='my_queue', durable=True)
# channel.basic_publish(exchange='', routing_key='my_queue', body='Hello, RabbitMQ!')
# print(" [x] Sent 'Hello, RabbitMQ!'")

# connection.close()

# import pika

# def callback(ch, method, properties, body):
#     print(f" [x] Received {body}")

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='my_queue', durable=True)

# channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()

# from faststream import FastStream
# from faststream.rabbit import RabbitBroker
# broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# app = FastStream(broker)

# @broker.subscriber("test-queue")  # название очереди RMQasync 
# def handle(msg: str):    
# 	print(msg)
 
#  @router.get("/data")
#  async def get_data():
#     clickhouse_connection = ClickHouseClient.connect(
#         host="127.0.0.1",
#         port=8123,
#         database="moex",
#         user="default",
#         password="default"
#     )
#     query = "SELECT * FROM data"
#     result = clickhouse_connection.execute(query)
#     data = [{"key": row[0], "value": row[1]} for row in result]
#     return {"data": data}

# #---------------------------------------------

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from fastapi import APIRouter
# import json
# import pika
# import uvicorn
# from faststream import FastStream
# from faststream.rabbit import RabbitBroker, RabbitQueue
# from clickhouse_driver import Client as ClickHouseClient

# app = FastAPI()
# router = APIRouter()

# @app.get("/")
# async def test() -> dict:
#     return {"message": "Тест"}

# broker = RabbitBroker(url="amqp://guest:guest@localhost:5672/")
# stream = FastStream(broker)

# class Data(BaseModel):
#     key: str
#     value: str
    
#     def to_dict(self):
#         return {"key": self.key, "value": self.value}
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(**data)
    
#     @staticmethod
#     def from_json(json_data):
#         return Data.from_dict(json.loads(json_data))
    
# @router.post("/send")
# async def send_data(data: Data):
#     serialized_data = json.dumps(data.to_dict())
#     await broker.publish(serialized_data, "data_queue")
#     return {"message": "Сообщение успешно отправлено"}

# @broker.subscriber(RabbitQueue(name="data_queue", durable=True))
# async def handle_message(data: str):
#     await handle_data(data)
# async def handle_data(data: str):
#     data = Data.from_json(data)
#     clickhouse_connection = ClickHouseClient.connect(
#         host="127.0.0.1",
#         port=8123,
#         database="moex",
#         user="default",
#         password="default"
#     )
#     query = f"INSERT INTO data (key, value) VALUES ('{data.key}', '{data.value}')"
#     ClickHouseClient.execute(query)
#     return {"message": "Данные успешно сохранены в ClickHouse"}

# @router.get("/data")
# async def get_data() -> dict:
#     try:
#         query = "SELECT * FROM data"
#         result = ClickHouseClient.execute(query)
#         data = [{"key": row[0], "value": row[1]} for row in result]
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# app.include_router(router)

# if __name__ == "__main__":  
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# --------------------------------------

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from fastapi import APIRouter
# import json
# import pika
# import uvicorn
# from faststream import FastStream
# from faststream.rabbit import RabbitBroker, RabbitQueue
# from clickhouse_driver import Client as ClickHouseClient

# app = FastAPI()
# router = APIRouter()

# @app.get("/")
# async def test() -> dict:
#     return {"message": "Тест"}

# class Data(BaseModel):
#     key: str
#     value: str
    
#     def to_dict(self):
#         return {"key": self.key, "value": self.value}
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(**data)
    
#     @staticmethod
#     def from_json(json_data):
#         return Data.from_dict(json.loads(json_data))
    
# # POST-метод /send, который принимает JSON-данные и отправляет их в очередь RabbitMQ.
    
# @router.post("/send")
# async def send_data(data: Data):
#     try:
#         serialized_data = json.dumps(data.model_dump())
#         rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
#         rabbitmq_channel = rabbitmq_connection.channel()
#         rabbitmq_channel.queue_declare(queue="data_queue")
#         rabbitmq_channel.basic_publish(exchange="", routing_key="data_queue", body=serialized_data)
#         rabbitmq_connection.close()
#         return {"message": "Сообщение передано успешно"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# # Функция, которая будет извлекать сообщения из очереди и отправлять их в ClickHouse для хранения.

# async def get_data_from_queue() -> dict:
#     rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
#     rabbitmq_channel = rabbitmq_connection.channel()
#     rabbitmq_channel.queue_declare(queue="data_queue")

#     clickhouse_connection = ClickHouseClient(host="127.0.0.1", port=8123, database="default", user="default", password="default")#+
#     while True:
#         method_frame, properties, body = rabbitmq_channel.basic_get(queue="data_queue", auto_ack=True)
#         if method_frame:
#             try:
#                 data = Data.from_json(body)
#                 query = f"INSERT INTO data (key, value) VALUES ('{data.key}', '{data.value}')"
#                 clickhouse_connection.execute(query)
#             except Exception as e:
#                 print(f"Error processing message: {str(e)}")
#         else:
#             break

#     rabbitmq_connection.close()
#     return {"message": "Очередь пуста"}

# # GET-метод /data, который будет извлекать данные из ClickHouse и возвращать их в формате JSON.

# @router.get("/data")
# async def get_data():
#     try:
#         query = "SELECT * FROM data"
#         clickhouse_connection = ClickHouseClient(host="127.0.0.1", port=8123, database="default", user="default", password="default")
#         result = clickhouse_connection.execute(query)
#         data = [{"key": row[0], "value": row[1]} for row in result]
#         return {"data": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))