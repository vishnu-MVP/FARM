from fastapi import FastAPI,Path,Body ,Header,UploadFile,File,Form
from pydantic import BaseModel
from enum import Enum
from typing import Dict
app =FastAPI()
#example for browser (client) display : from database --> (here) backend FASTAPI ---> (browser)frontend data
@app.get("/")
async def root():
    return {"message":"Home page get"}

#example for insomnia usage : GUI to analyse other than get methods

@app.post("/post")
async def hello_world():
    return {"message":"posted sucessfully"}

#example for docs usage + (non type hinting cons):to test api endpoints

@app.get("/car/{c_id}")
async def id(c_id):
    return {"Car_id":c_id}

#example for type hinting : to prevent wrong data entry by users to database

@app.get("/cars/{c_id}")
async def tid(c_id:int): #type hinted
    return {"Car_id":c_id}

#example for path and enum usage to prevent path manipulation
class membership(str,Enum):
    FREE="free"
    PRO="pro"

@app.get("/acc/{mem}/{mon}")
async def account(mem:membership,mon:int=Path(...,ge=3,le=12)):
    return{
        "message":"Account created",
        "type":mem,
        "months":mon
    }

#example for query parameters : like searching for a particular page ( like washing machine prices from 2000 to 15000)
#order is necessary
@app.get("/pcars/price") # here bug was in /cars , as used above with other type hinted path , so changed to unique path name pcars
async def cars_by_price(min_price: int=0, max_price:int=100000):
    return{"Message":f"Listing cars with prices between {min_price} and {max_price}"}

# example for post request : getting from user and both displaying to them (browser) and sending to database

# its done with run time validation using pydantic --one of the best features of fastapi

class insertcar(BaseModel):
    brand:str
    name:str
    cid:int

@app.post("/postc")
async def postcar(data: insertcar=Body(...)): #mistake in book ,Dict  need to be imported from typing also its mandatory for Dict though not used 
#insomnia is used exactly here , to type lines of code easily
    return{"success":data}

#now we successfully learnt to get input from user and displayed it to them , but it just type casted as per hints , doesnt throw error 

'''pending learnings :
    1.How to link our cloud database
    2. how to put these inputs to database
    3. how to get the previously stored data from database and show it to users 


 these we will learn from chapter 5 : when we start integrating MongoDb with FASTAPI to show/obtain data to user Interface , which is react
'''

#now lets see basics of headers , cookies and form data and files

# 1. headers : contains info about user , cookies : saves the state ---> like cart items , previously searched items in a search bar , unexpired login sessions 

# 2. form data is to get respective field data from a user entered form (from frontend), which includes pictures and files

@app.get("/headers")
async def get_header(user_agent:str|None=Header(None)): #bug here is should not use "user" as such words are system pre-defined
    return{"user is :":user_agent}

#form multipart

@app.post("/upload")
async def fupload(file:UploadFile=File(...) , brand:str=Form(...),model:str=Form(...),year:int=Form(...)):
    return{
        "brand":brand,
        "model":model,
        "file name":file.filename 
    }


#########################        Lets build some good looking Frontend              ###############################################

#Intro to react :

'''
        1. All frontend applications are web (web browser) interacting 

        2. So whenever we need interaction in website , like clicking "follow" button turns it into "followed" , or when we click like button for a video , it turns blue , all mouse hovering (moving) interactions , all scrolling interactions , everything is implemented with "javascripts" --> the language of web


        3. Its very hard to build interactions from scratch , like hard programming "print" function from scratch , rather than just using print() function .

        4. SO just like this pre-defined print() function , we will use pre-defined library which simplifies JS implementation, which is the React 

'''