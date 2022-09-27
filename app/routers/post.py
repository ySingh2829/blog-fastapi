from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(
        prefix="/posts"
)

# Get all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Get one posts
@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')
    return post

@router.post("/", status_code=status.HTTP_201_CREATED,
        response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int ,post: schemas.PostCreate,
        db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    test_post = post_query.first()
    if test_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return test_post
