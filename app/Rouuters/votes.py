from fastapi import APIRouter,HTTPException
from .. import schema,database,models
from sqlalchemy.orm import Session
from fastapi import Body, Depends,status
from . import oath2

router=APIRouter(
    
    prefix='/vote',
    tags=['Vote System']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def add_vote(vote:schema.Vote, db: Session = Depends(database.get_db), current_user:str=Depends(oath2.get_current_user)):
    post=db.query(models.Posts).filter(models.Posts.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This post doesn't exist")
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    vote_result=vote_query.first()
    if vote.vote_dir ==1:
        if vote_result:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This user has already voted") 
        new_vote=models.Votes(user_id=current_user.id,post_id=vote.post_id)   
        db.add(new_vote)
        db.commit()
        return "Vote is added successfully"
    else:
        if not vote_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote doesn't exist")
        if vote_result:
            vote_query.delete(synchronize_session=False)
            db.commit()    
        return {"message":"Vote is deleted successfully"}



