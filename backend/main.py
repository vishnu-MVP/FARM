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
router =APIRouter()
app = FastAPI()
app.include_router(cars_router,prefix='/cars',tags=['cars'])
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


#Inserting into the database
    
@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase =Body(...)):
    car = jsonable_encoder(car)
    new_car = await request.app.mongodb["cars"].insert_one(car)
    created_car = await request.app.mongodb["cars"].find_one({"_id": new_car.inserted_id}
)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=created_car)

####### End of insertion

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()



if __name__ == "__main__":
    uvicorn.run(
    "main:app",
    reload=True
)