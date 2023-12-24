'''from fastapi import APIRouter,Request,HTTPException,status,Body
from fastapi.encoders import jsonable_encoder 
from fastapi.responses import JSONResponse
from models import CarDB,CarBase,CarUpdate
from typing import Optional,List
from bson import objectid
#Displaying all from Database 
router = APIRouter()
@router.get("/", response_description="List all cars") #-----> Read general + search by brand
async def list_all_cars(request:Request , min_price:int=0, max_price:int=100000,brand:Optional[str]=None,page:int=1) -> List[CarDB]:
    RESULTS_PER_PAGE = 25
    skip = (page-1)*RESULTS_PER_PAGE
    query = {"price":{"$lt":max_price, "$gt":min_price}}
    if brand:
        query["brand"] = brand
    full_query = request.app.mongodb['cars'].find(query).sort("_id",-1).skip(skip).limit(RESULTS_PER_PAGE)
    raw_cars = await full_query.to_list(length=RESULTS_PER_PAGE)
    results = []
    for raw_car in raw_cars:
        # Filter out keys not present in the CarDB model
        valid_car_data = {key: raw_car[key] for key in raw_car if key in CarDB.__fields__}
        results.append(CarDB(**valid_car_data))
    
    return results



#Inserting into the database -----> Create
    

@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase =Body(...)):
    car = jsonable_encoder(car)
    new_car = await request.app.mongodb["cars"].insert_one(car)
    created_car = await request.app.mongodb["cars"].find_one({"_id": new_car.inserted_id}
)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=created_car)


####### End of insertion


### Retrieving from the database ###### ------> Read Particular

@router.get("/{id}",response_description="getting a single car")
async def show_car(id:str,request:Request):
    car = await request.app.mongodb["cars"].find_one({"_id": id})
    if car:
        valid_car_data = {key: car[key] for key in car if key in CarDB.__fields__}
        return CarDB(**valid_car_data)
    else:
        raise HTTPException(status_code=404, detail=f"Car with ID {id} not found")

### End of Retrieving #######

### Updating data  ######### -----------> Update operation

@router.patch("/{id}",response_description="Update a car")
async def update_car(id:str,request:Request ,car_update:CarUpdate=Body(...)):
        # Perform the update operation
        await request.app.mongodb["cars"].update_one(
            {"_id":id},
            {"$set": car_update.dict(exclude_unset=True)}
        )
        # Retrieve the updated car details
        updated_car = await request.app.mongodb["cars"].find_one({"_id":id})
        if updated_car:
            # Return the updated details
            valid_car_data = {key: updated_car[key] for key in updated_car if key in CarDB.__fields__}
            return CarDB(**valid_car_data)
        else:
            raise HTTPException(status_code=404, detail=f"Car with ID {id} not found")
            '''

from typing import Tuple, List, Optional

from fastapi import APIRouter, Request, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from models import CarBase, CarDB, CarUpdate


router = APIRouter()

@router.get("/", response_description="List all cars")
async def list_all_cars(
    request: Request, 
    min_price: int=0, 
    max_price:int=100000, 
    brand: Optional[str] = None,
    page:int=1,
    ) -> List[CarDB]:

    RESULTS_PER_PAGE = 25
    skip = (page-1)*RESULTS_PER_PAGE
    
    
    query = {"price":{"$lt":max_price, "$gt":min_price}}
    if brand:
        query["brand"] = brand
    
    full_query = request.app.mongodb['cars1'].find(query).sort("_id",-1).skip(skip).limit(RESULTS_PER_PAGE)

    results = [CarDB(**raw_car) async for raw_car in full_query]

    # this is also possible
    # results = await full_query.to_list(1000)
    
    return results

# create new car
@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    car = jsonable_encoder(car)
  
    new_car = await request.app.mongodb["cars1"].insert_one(car)
    created_car = await request.app.mongodb["cars1"].find_one(
        {"_id": new_car.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)

# get car by ID
@router.get("/{id}", response_description="Get a single car")
async def show_car(id: str, request: Request):
    if (car := await request.app.mongodb["cars1"].find_one({"_id": id})) is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")

@router.patch("/{id}", response_description="Update car")
async def update_task(id: str, request: Request, car: CarUpdate = Body(...)):
  
    await request.app.mongodb['cars1'].update_one(
        {"_id": id}, {"$set": car.dict(exclude_unset=True)}
    )

    if (car := await request.app.mongodb['cars1'].find_one({"_id": id})) is not None:
        return CarDB(**car)

    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.delete("/{id}", response_description="Delete car")
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb['cars1'].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

    raise HTTPException(status_code=404, detail=f"Car with {id} not found")




# optional
@router.get("/brand/{brand}", response_description="Get brand overview")
async def brand_price(brand: str,request: Request):

    query = [
        {
            '$match': {
                'brand': brand
            }
        }, {
            '$project': {
                '_id': 0, 
                'price': 1, 
                'year': 1, 
                'make': 1
            }
        }, {
            '$group': {
                '_id': {
                    'model': '$make'
                }, 
                'avgPrice': {
                    '$avg': '$price'
                }
            }, 
        }, {
            '$sort': {
                'avgPrice':1
            }
        }
    ]

    full_query = request.app.mongodb['cars1'].aggregate(query)

    results = [el async for el in full_query]
    
    return results