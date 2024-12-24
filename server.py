import uvicorn
from fastapi import FastAPI


from routers.fastapi_task import fastapi_task_router

app = FastAPI()

app.include_router(fastapi_task_router, prefix="/main")


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=5000, reload=True)