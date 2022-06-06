from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from typing import Union
from enum import Enum
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

df = pd.read_csv('dataset.csv', index_col=0)

@app.get("/")
async def root():
    return {"message" : "Index Page"}

@app.get("/data")
async def load_data(page_num: int = 1, page_size: int = 10):
    data = df.to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]

@app.get("/data/{order_by}")
async def get_data(order_by: str = "TransactionDate", page_num: int = 1, page_size: int = 10):
    data = df.sort_values(by=[f'{order_by}'], ascending=False).to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]

@app.get('/item/{name}')
async def find_commodity(commodity_name: str,  page_num: int = 1, page_size: int = 10):
    data = df.loc[df['Commodity'] == commodity_name]
    data = data.to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]
