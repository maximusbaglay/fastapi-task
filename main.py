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

# faststream run main:app

# from database.connection import client  
  
 
# if __name__ == "__main__":  
#     result = client.query('SELECT * FROM records')  
#     print(result.result_rows)
    
    
    
#     get_data



# Запуск RabbitMQ и сервера.
# faststream run main:app
# python serve.py

from database.connection import client


if __name__ == "__main__":
    result = client.query('SELECT * FROM records')
    print(result.result_rows)