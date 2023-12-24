#Integration tutorial --part 2

from decouple import config
import uvicorn
DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routers.cars import router as cars_router
from fastapi import APIRouter, Request, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import CarBase
from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost",
"http://localhost:8080",
"http://localhost:3000",
"http://localhost:8000",
]
router =APIRouter()
app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.include_router(cars_router,prefix='/cars',tags=['cars'])
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]




@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()



if __name__ == "__main__":
    uvicorn.run(
    "main:app --host 0.0.0.0 --port 10000",
    reload=True
)