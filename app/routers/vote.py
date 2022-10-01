from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
        current_user = Depends(oauth2.get_current_user)):

    # If there is no post for that specific id, send 404 error
    post =  db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: {vote.post_id} does not exist")

    # Find the post with requested_post's id and current_user's id
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id)
    found_post = vote_query.first()

    if vote.dir == 1:
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                    detail=f'user {current_user.id} has already voted on post {found_post.post_id}')

        # If not found, add to the database
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Vote does not exist")

        # if found post delete
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
