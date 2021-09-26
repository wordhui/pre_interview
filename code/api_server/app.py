import re
import sys
import datetime
from pathlib import Path
from decimal import Decimal
from typing import List, Dict

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Body, Response
from fastapi.middleware.cors import CORSMiddleware

from middleware import LimitUploadSize
from tags_metadata import api_tags_metadata

base_dir = Path(__file__).parent.parent
run_argv = sys.argv[0]
DEBUG = None
if run_argv.split('/')[-1] == 'app.py':
    DEBUG = True
else:
    DEBUG = False
if DEBUG:
    app = FastAPI(openapi_tags=api_tags_metadata)
else:
    # app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app = FastAPI(openapi_tags=api_tags_metadata)  # 此处采用这种模式是方便部署到云服务器查看 api文档页面


class AddInputList(BaseModel):
    value_array: List[Dict[str, float]]


class ChatMsg(BaseModel):
    msg: str = Body(..., max_length=5 * 1024 * 1024)


@app.on_event('startup')
async def startup():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=['*'],
    )
    app.add_middleware(LimitUploadSize, max_upload_size=5 * 1024 * 1024)  # 限制接口请求数据大小为5M


@app.post('/add', tags=['add'])
async def add(args: AddInputList, response: Response):
    """"""
    result = Decimal('0')
    for data_item in args.value_array:
        result += Decimal(str(data_item.get('value')))
    return {'result': float(result)}


@app.get('/get_date', tags=['get_date'])
async def get_date():
    beijing_timezone = datetime.timezone(datetime.timedelta(hours=8))
    beijing_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone(beijing_timezone).date()
    return {'date': beijing_date}


@app.post('/chat', tags=['chat'])
async def chat(args: ChatMsg):
    # if re.search(r'(?isu)您好.*?再见|再见.*?您好', args.msg): # 长文本性能过差
    #     return {'result': '天气不错。'}
    key = 0
    msg_dict = {0: '', 1: '您好，您吃了吗？', 3: '回见了您内。', 4: '天气不错。'}
    if re.search(r'(?isu)您好', args.msg):
        key += 1
    if re.search(r'(?isu)再见', args.msg):
        key += 3
    return {'result': msg_dict[key]}


def main():
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
