from typing import Optional,List
from fastapi import Body, Depends, FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy import null,func
from .. import schema
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. import models
from ..database import Session_Local, engine
from sqlalchemy.orm import Session
from .. import utils
from ..database import get_db
from . import oath2
from sqlalchemy.orm import joinedload
import json



router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# creation of tables using Base this line will create all the tables that are mentioned inside models
models.Base.metadata.create_all(bind=engine)









# BEFORE THE DATABASE
# Array of posts
my_list=[{"title":"this is our title","content":"all this is content ","id":1},
{"title":"This is our second title","content":"the is the content of second post","id":2}
]    


# First root path
# @router.get("/")
# def read_root():
#     return {"Hello": "welcome to "}


# Get all the data from this list
# @router.get('/getposts')
# def get_posts():
#     return {"hello":my_list}
   

# Create post
# @router.post("/createpost",status_code=status.HTTP_201_CREATED)
# def create_post(payload:Post):
#     my_post=payload.dict()
#     my_post['id']=randrange(0,1000000)
#     my_list.append(my_post)
#     return my_list


#Function to iterate over the complete array and look for one specific post
# def get_one_post(id):
#     b=int(id)
#     for p in my_list:
#         if(p["id"]==b):
#             return p


# Get Latest Post            
# @router.get('/posts/latest')
# def get_latest_post():
#     post=my_list[len(my_list)-1]
#     return {"result": post}


# Get one post
# @router.get('/getpost/{id}')
# def getposts(id):
#     post=get_one_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this post is not found")
#     else:
#      return {" Result ": post}  


# Delete Post
# def delete_item(id):
#     for index,item in enumerate(my_list):
#         if(item['id']==id):
#             return index


# Delete post 
# @router.delete('/deletepost/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     ind=delete_item(id)
#     if ind== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not found")
#     my_list.pop(ind)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# Function
# def find_post_by_id(id):
#     for index,values in enumerate(my_list):
#         if(values['id']==id):
#             return index


# for updating a post
# @router.put('/updatepost/{id}') 
# def updatepost(id:int,post:Post):
    # index=find_post_by_id(id)

    # if index==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # else :
    #     post_dict=post.dict()
    #     post_dict['id']=id
    #     my_list[index]=post_dict

    #     return {"result":my_list[index]}
# BEFORE THE DATABASE


# AFTER THE DATABASE CONNECTION
# Route to get all the posts from the database
# @router.get('/getposts')
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     # for post in posts:
#     print(posts)
#     return {'posts':posts}


# For creating a brand new post
# @router.post('/createpost')
# def create_post(post:Post):
#     cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING*", (post.title, post.content))
#     new_post=cursor.fetchone()
#     connection.commit() 
#     return {"result":new_post}

# getting a post with specific id
# @router.get('/getonepost/{id}')
# def get_one_post(id:int):
#     cursor.execute("SELECT * from posts WHERE id=%s",(id,))
#     one_post=cursor.fetchone()
#     if not one_post:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="piece of information is not present")
#     return one_post

# Deleting a post
# @router.delete('/deletepost/{id}',status_code=status.HTTP_202_ACCEPTED)
# def delete_post(id:int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,)) 
#     deletedpost=cursor.fetchone()
#     if not deletedpost:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not present")
#     connection.commit()
#     return deletedpost

# Update a post
# @router.put('/updatepost/{id}')
# def update_post(post:Post,id:int):
#     cursor.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING*", (post.title, post.content,id))
#     connection.commit()
#     update_post=cursor.fetchone()
#     if not update_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
#     return update_post



# using sql alchemy for all the operations
# using orm for path operations
# path operation to get all the data from the databse
@router.get('/')
# def get_posts(db: Session = Depends(get_db),current_user:str=Depends(oath2.get_current_user)):
#     post = db.query(models.Posts).all()
#     if not post:
#         raise HTTPException(status_code=404, detail="No posts found.")
#     return [p.__dict__ for p in post]
def get_posts(db: Session = Depends(get_db),
current_user:str=Depends(oath2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # post = db.query(models.Posts).filter(models.Posts.title.ilike(f"%{search}%")).options(
    #     joinedload(models.Posts.owner)).limit(limit=limit).offset(skip).all()
    result = db.query(models.Posts, func.count(models.Votes.post_id).label("number_of_votes"))\
        .outerjoin(models.Votes, models.Posts.id==models.Votes.post_id)\
            .group_by(models.Posts.id).filter(models.Posts.title.ilike(f"%{search}%")).limit(limit=limit).offset(skip).all()
    if not result:
        raise HTTPException(status_code=404, detail="No posts found.")
    # return query
    # return [schema.GetAllPost(title=p.title, content=p.content, published=p.published,
    #  owner_id=p.owner_id, id=p.id, created_at=p.created_at,
    #   owner=schema.ReturnUser(email=p.owner.email,id=p.owner.id,created_at=p.created_at)) for p in post]
    post_response = []
    for p, votes in result:
        post_response.append(
        schema.GetAllPost(
            title=p.title,
            content=p.content,
            published=p.published,
            owner_id=p.owner_id,
            id=p.id,
            created_at=p.created_at,
            owner=schema.ReturnUser(
                email=p.owner.email, id=p.owner.id, created_at=p.created_at
            ),
            votes = votes
        )
    )
    response = schema.GetAllPostResponse(post=post_response)
    return response


# paht operation to get one specific post from the data with its id and to get the user who created this post
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schema.GetAllPostResponse)
def get_posts(id:int, db: Session = Depends(get_db)):
    # post = db.query(models.Posts).filter(models.Posts.id==id).options(joinedload(models.Posts.owner)).first()
    result = db.query(models.Posts, func.count(models.Votes.post_id).label("number_of_votes"))\
        .outerjoin(models.Votes, models.Posts.id==models.Votes.post_id)\
        .filter(models.Posts.id==id)\
        .group_by(models.Posts.id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Post not found.")  
    # return schema.GetAllPost(title=post.title, content=post.content, published=post.published,
    #     owner_id=post.owner_id, id=post.id, created_at=post.created_at,
    #     owner=schema.ReturnUser(email=post.owner.email,id=post.owner.id,created_at=post.created_at))
    post_response = []
    for p, votes in result:
        post_response.append(
        schema.GetAllPost(
            title=p.title,
            content=p.content,
            published=p.published,
            owner_id=p.owner_id,
            id=p.id,
            created_at=p.created_at,
            owner=schema.ReturnUser(
                email=p.owner.email, id=p.owner.id, created_at=p.created_at
            ),
            votes = votes
        )
    )
    response = schema.GetAllPostResponse(post=post_response)
    return response  



# Path operation for creating a post   
@router.post('/',response_model=schema.ReturnPost)
def createpost(post:schema.Create_post,db: Session = Depends(get_db),current_user:str=Depends(oath2.get_current_user)):
    print(current_user.email)
    newpost=models.Posts(**post.dict())
    newpost.owner_id=current_user.id
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost.__dict__


# Delete path operation
@router.delete('/{id}')
def deletepost(id:int,db: Session = Depends(get_db),current_user:str=Depends(oath2.get_current_user)):
    post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not present")
    print(post)
    if post.owner_id ==current_user.id:
        db.delete(post)
        db.commit()
        return "Post is deleted successfully"
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This post is not created by the current user")    
    
# path operation for updating a post:
@router.put('/{id}',response_model=schema.ReturnPost)
def update_post(post:schema.UpdatePost, id:int,db: Session = Depends(get_db),current_user:str=Depends(oath2.get_current_user)):
    posttoupdate=db.query(models.Posts).filter(models.Posts.id==id)
    reterievedpost=posttoupdate.first()
    if not reterievedpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post doesn't exist")
    if reterievedpost.owner_id ==current_user.id:    
        posttoupdate.update(post.dict(),synchronize_session=False)   
        db.commit() 
        return posttoupdate.first().__dict__
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="This current user is not allowed to update this post")



















