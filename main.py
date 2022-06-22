import io
import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from typing import Union
from enum import Enum
import matplotlib.image as mpimg
from numpy import imag
import cv2
from pydantic import BaseModel
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from starlette.responses import StreamingResponse
import linear_regression

app = FastAPI()

df = pd.read_csv('dataset.csv', index_col=0)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@repeat_every(seconds=31536000)  # 1 year in seconds: 31536000
def remove_expired_tokens_task() -> None:
    linear_regression.predict()


@app.get("/")
async def root():
    return {"message": "Index Page"}


@app.get("/data")
async def load_data(page_num: int = 1, page_size: int = 10):
    data = df.to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]


@app.get("/data/{order_by}")
async def get_data(order_by: str = "TransactionDate", page_num: int = 1, page_size: int = 10):
    data = df.sort_values(by=[f'{order_by}'],
                          ascending=False).to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]


@app.get('/commodity/name/{commodity_name}')
async def find_commodity_by_name(commodity_name: str,  page_num: int = 1, page_size: int = 10):
    data = df.loc[df['Commodity'] == commodity_name]
    data = data.to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]


@app.get('/commodity/city/{commodity_city}')
async def find_commodity_by_city(commodity_city: str,  page_num: int = 1, page_size: int = 10):
    data = df.loc[df['City'] == commodity_city]
    data = data.to_dict(orient="records")
    start = (page_num - 1) * page_size
    end = start + page_size
    return data[start:end]


@app.get('/commodity/{commodity_id}')
async def find_commodity_by_id(commodity_id: int):
    data = df.loc[df['ID'] == commodity_id]
    data = data.to_dict(orient="records")
    return data


@app.get('/price-prediction-image/{commodity_name}', response_class=FileResponse)
async def get_prediction_image_by_commodity_name(commodity_name: str):
    images_path = './images/'
    images = next(os.walk(images_path))[2]

    for image in images:
        if commodity_name.lower() not in image.lower():
            continue

        file = images_path + image
        return file

    return {"message": "the file doesn't exist"}
