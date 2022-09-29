from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                user='yash33', password='crane_k1Ck',
                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_data = [{"title": "Welcome", "content": "This site uses fastapi", "id": 1},
        {"titile": "title2", "content": "I like pizza", "id": 2}]            
       
def find_post(id):
    for item in my_data:
        if item["id"] == id:
            return item

def find_index(id):
    for i, item in enumerate(my_data):
        if item["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Root
@app.get("/")
def root():
    return {"message": "Hello, from api"}


