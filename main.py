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
from faststream.rabbit import RabbitBroker
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
    

@router.post("/send")
async def send_data(data: Data):
    serialized_data = json.dumps(data.to_dict())
    await broker.publish(serialized_data, "data_queue")
    return {"message": "Сообщение успешно отправлено"}

@router.get("/data")
async def get_data():
    clickhouse_connection = ClickHouseClient.connect(
        host="127.0.0.1",
        port=8123,
        database="fastapi_task",
        user="default",
        password="default"
    )
    query = "SELECT * FROM data"
    result = clickhouse_connection.execute(query)
    data = [{"key": row[0], "value": row[1]} for row in result]
    return {"data": data}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)