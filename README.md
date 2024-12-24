1. **Установка необходимых библиотек**

```
pip install fastapi
```

```
pip install clickhouse-connect
```

```
pip install "faststream[rabbit]" "faststream[cli]" fastapi pydantic-settings
```

2. **Настройка RabbitMQ**:

Запуск RabbitMQ:
```
faststream run rabbit.subscriber:app 
```

Запуск FastAPI и FastStream:
```
faststream run rabbit.subscriber:app 
```

Запуск сервера:
```
python server.py
```

3. **FastAPI приложение**:

   - В файле `main.py` реализованы следующие функции:

     - **Endpoint для отправки данных**:

       - POST-метод `/send`, который принимает JSON-данные и отправляет их в очередь RabbitMQ.

       ```
       @router.post("/send")
       ```
       
     - **Функция для обработки сообщений**:

       - Функция, которая будет извлекать сообщения из очереди и отправлять их в ClickHouse для хранения.

       ```
       async def get_data_from_queue() -> dict:
       ```
       
     - **Endpoint для получения данных**:
     
       - GET-метод `/data`, который будет извлекать данные из ClickHouse и возвращать их в формате JSON.
       
       ```
       @router.get("/data")
       ```