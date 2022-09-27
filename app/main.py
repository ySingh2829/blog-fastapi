from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='yash33',
                password='crane_k1Ck', cursor_factory=RealDictCursor)
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

# Root
@app.get("/")
def root():
    return {"message": "Hello, from api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}

# Get all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# Get one posts
@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT id, title, content, published, created_at FROM posts WHERE id = %s """,
    #        (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #        (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    #deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int ,post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s""",
    #        (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    test_post = post_query.first()
    if test_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return test_post
