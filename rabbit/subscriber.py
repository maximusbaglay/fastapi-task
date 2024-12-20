from faststream import FastStream  
from faststream.rabbit import RabbitBroker, RabbitQueue  
from loguru import logger  
  
from config.settings import settings  
  
  
broker = RabbitBroker(url=settings.rabbit_url)  
app = FastStream(broker)  
  
  
@broker.subscriber(RabbitQueue(name="settings.queue_tasks", durable=True))  
async def task(ticker: str):  
    logger.success(ticker)