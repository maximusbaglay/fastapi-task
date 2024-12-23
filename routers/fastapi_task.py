# from fastapi import APIRouter  
  
# from rabbit.publisher import publish_task_ticker  
  
# fastapi_task_router = APIRouter(tags=["fastapi_task"])  
  
# @fastapi_task_router.get("/{ticker}")  
# async def retrieve_all_records(ticker: str) -> dict:  
#     await publish_task_ticker(ticker=ticker)  
#     return {"message": "the ticker has been successfully added to the queue"}