from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
import json
import pika
import uvicorn
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from clickhouse_driver import Client

app = FastAPI()
router = APIRouter()

@app.get("/")
async def test() -> dict:
    return {"message": "Тест"}

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
    try:
        serialized_data = json.dumps(data.model_dump())
        rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
        rabbitmq_channel = rabbitmq_connection.channel()
        rabbitmq_channel.queue_declare(queue="data_queue")
        rabbitmq_channel.basic_publish(exchange="", routing_key="data_queue", body=serialized_data)
        rabbitmq_connection.close()
        return {"message": "Сообщение передано успешно"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_data_from_queue() -> dict:
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.queue_declare(queue="data_queue")
    while True:
        method_frame, properties, body = rabbitmq_channel.basic_get(queue="data_queue", auto_ack=True)
        if method_frame:
            try:
                data = Data.from_json(body)
                query = f"INSERT INTO data (key, value) VALUES ('{data.key}', '{data.value}')"
            except Exception as e:
                print(f"Ошибка: {str(e)}")
        else:
            break
    rabbitmq_connection.close()
    return {"message": "Очередь пуста"}

@router.get("/data")
async def get_data():
    try:
        query = "SELECT * FROM data"
        data = [{"key": row[0], "value": row[1]} for row in query]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))