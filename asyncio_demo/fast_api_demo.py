import asyncio
import time

import uvicorn
from fastapi import FastAPI

import pydantic
from pydantic import BaseModel


class Hello(BaseModel):
    id: int
    msg: str

app = FastAPI()


# statuses = {
#     '123nfdgfdsjg': {'status': 'processing', 'path': None}
# }

@app.post('/api/upload')
async def upload():
    pass

    #Popen(ffmpeg)

@app.get('/api/long')
async def hello():
    time.sleep(30)
    return {'msg': 'Hi', 'id': 1}
    # return Hello(id=1, msg='Hi')


@app.get('/api/hello')
async def hello():
    # time.sleep(30)
    # return {'msg': 'Hi', 'id': 1}
    await asyncio.sleep(3)
    return Hello(id=1, msg='Hi')

if __name__ == '__main__':
    uvicorn.run(app)