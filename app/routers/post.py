from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
        prefix="/posts",
        tags=['Posts']
)

# Get all posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, 
        skip: int = 0, search: Optional[str] = ""):

    # Perform LEFT JOIN on posts and votes and count total votes per post
    results = db.query(models.Post, func.count(models.Vote.post_id).label("total_votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f'%{search}%')).limit(limit).offset(skip).all()

    return results

# Get one posts
@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("total_votes")).join(models.Vote, 
            models.Vote.post_id == models.Post.id, 
            isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')

    return post

@router.post("/", status_code=status.HTTP_201_CREATED,
        response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int ,post: schemas.PostCreate,
        db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    test_post = post_query.first()
    if test_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f'post with id: {id} was not found')

    if test_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return test_post
