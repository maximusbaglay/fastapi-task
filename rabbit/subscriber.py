import json
import time

from faststream import FastStream  
from faststream.rabbit import RabbitBroker, RabbitQueue  
from loguru import logger  
  
from config.settings import settings  
  
  
broker = RabbitBroker(url=settings.rabbit_url)  
app = FastStream(broker)  
  
  
@broker.subscriber(RabbitQueue(name="settings.queue_tasks", durable=True))  
async def task(ticker: str):
    logger.info(f"Start ticker {ticker}")
    data = []
    for row in app.get_data(ticker):
        data.append(json.dumps(row))
        
    with open(DATA_DIR / f"{ticker}_{int(time.time())}.json", "w") as f:
        json.dump(data, f)
    # logger.success(ticker)