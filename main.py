# Цель задания

# Создать простое приложение на FastAPI, которое будет использовать RabbitMQ для асинхронной обработки сообщений и ClickHouse для хранения и анализа данных.
# Задание
# Установите необходимые библиотеки
# Настройка RabbitMQ:

#     Установите RabbitMQ и убедитесь, что он запущен.
#     Создайте очередь для обработки сообщений, например, data_queue.

# Создайте FastAPI приложение:

#     Создайте файл main.py и реализуйте следующие функции:
#         Endpoint для отправки данных:
#             Создайте POST-метод /send, который принимает JSON-данные и отправляет их в очередь RabbitMQ.
#         Функция для обработки сообщений:
#             Создайте функцию, которая будет извлекать сообщения из очереди и отправлять их в ClickHouse для хранения.
#         Endpoint для получения данных:
#             Реализуйте GET-метод /data, который будет извлекать данные из ClickHouse и возвращать их в формате JSON.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
import json
import pika
import uvicorn
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from clickhouse_driver import Client as ClickHouseClient

app = FastAPI()
router = APIRouter()

@app.get("/")
async def test() -> dict:
    return {"message": "Тест"}

broker = RabbitBroker(url="amqp://guest:guest@localhost:5672/")
stream = FastStream(broker)

class Data(BaseModel):
    key: str
    value: str
    
    def to_dict(self):
        return {"key": self.key, "value": self.value}
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    @staticmethod
    def from_json(json_data):
        return Data.from_dict(json.loads(json_data))
    
@router.post("/send")
async def send_data(data: Data):
    serialized_data = json.dumps(data.to_dict())
    await broker.publish(serialized_data, "data_queue")
    return {"message": "Сообщение успешно отправлено"}

@broker.subscriber(RabbitQueue(name="data_queue", durable=True))
async def handle_message(data: str):
    await handle_data(data)
async def handle_data(data: str):
    data = Data.from_json(data)
    clickhouse_connection = ClickHouseClient.connect(
        host="127.0.0.1",
        port=8123,
        database="moex",
        user="default",
        password="default"
    )
    query = f"INSERT INTO data (key, value) VALUES ('{data.key}', '{data.value}')"
    ClickHouseClient.execute(query)
    return {"message": "Данные успешно сохранены в ClickHouse"}

@router.get("/data")
async def get_data() -> dict:
    try:
        query = "SELECT * FROM data"
        result = ClickHouseClient.execute(query)
        data = [{"key": row[0], "value": row[1]} for row in result]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)

if __name__ == "__main__":  
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# faststream run rabbit.subscriber:app  
# faststream run main:app
# python server.py
# Ctrl+C для остановки FastAPI и RabbitMQ.