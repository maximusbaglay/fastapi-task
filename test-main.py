# Домашнее задание: Интеграция RabbitMQ, ClickHouse и FastAPI
# Цель задания
# Создать простое приложение на FastAPI, которое будет использовать RabbitMQ для асинхронной обработки сообщений и ClickHouse для хранения и анализа данных.

# Задание
# Установите необходимые библиотеки
# Настройка RabbitMQ:
# Установите RabbitMQ и убедитесь, что он запущен.
# Создайте очередь для обработки сообщений, например, data_queue.
# Создайте FastAPI приложение:
# Создайте файл main.py и реализуйте следующие функции:
# Endpoint для отправки данных:
# Создайте POST-метод /send, который принимает JSON-данные и отправляет их в очередь RabbitMQ.
# Функция для обработки сообщений:
# Создайте функцию, которая будет извлекать сообщения из очереди и отправлять их в ClickHouse для хранения.
# Endpoint для получения данных:
# Реализуйте GET-метод /data, который будет извлекать данные из ClickHouse и возвращать их в формате JSON.
# Тестирование:
# Используйте Postman или curl для отправки POST-запроса на /send с JSON-данными.
# Запустите функцию обработки сообщений в отдельном потоке или процессе, чтобы она постоянно обрабатывала новые сообщения.
# Проверьте, что данные успешно сохраняются в ClickHouse, и используйте GET-запрос на /data для их получения.
import clickhouse_connect
from loguru import logger

# запрос из базы данных для бд moex

client = clickhouse_connect.get_client(host='127.0.0.1', port=8000, username='default', database="test")

if __name__ == "__main__":  
    result = client.query('SELECT * FROM records limit 10')
    for row in result.result_rows:
        logger.info(row)


# На debian создать заново
# Отправка не через pika, а через faststream
# Отправка сообщений
# Получение сообщений

# Запуск фастстрим
# faststream run main:app

# Добавить
# from faststrea.CLI import а пикуц убрать


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
import json
import pika
import clickhouse_driver
import uvicorn
from faststream import FastStream
from faststream.rabbit import RabbitBroker

app = FastAPI()
router = APIRouter()

@app.get("/")
async def test() -> dict:
    return {"message": "Тестирование"}

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

clickhouse_connection = clickhouse_driver.connect(
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
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="175.0.0.1", port=8000)
#     rabbitmq_connection.close()
#     clickhouse_connection.close()
#     clickhouse_driver.disconnect()
#     print("RabbitMQ and ClickHouse connections closed")