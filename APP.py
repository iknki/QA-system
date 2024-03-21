import time

from fastapi import FastAPI

#from config.config import Config
#from llmmodel.model import Model

app = FastAPI()
#config = Config("./config.yaml")
#Model(config)

@app.get("/api/status")
def status():
    return {"status": "ok"}

async def QA():
    start_time = time.time()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/post")
async def post():
    return {"message": "Hello World"}
@app.get("/api/get")
async def get():
    return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
