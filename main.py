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
