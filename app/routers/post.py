#region Import Libraries
from fastapi import FastAPI,Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, utils , oauth2
from typing import List,Optional
from ..database import engine, get_db
from sqlalchemy import func
#endregion Import Libraries

router = APIRouter(
     prefix = "/posts",
     tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,skip:int=0,search: Optional[str] = ""):
     # print(search)
     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
     result_temp = db.query(models.Post)
     result = [r for r in results]
     print(results)
     # result = [r for r in results] 
     
     return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
#here payload extracts all the values from the body
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     # new_post = models.Post(title=post.title,content=post.content,published = post.published)
     print(current_user.email)
     new_post = models.Post(owner_id = current_user.id , **post.dict())
     db.add(new_post)
     db.commit()
     db.refresh(new_post)
     return new_post
      
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int, db:Session =Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
     #get_post_by_id = db.query(models.Post).filter(models.Post.id == id).first()
     get_post_by_id =  db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
     if not get_post_by_id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
         
      
     return get_post_by_id

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
     
     post_query = db.query(models.Post).filter(models.Post.id == id)
     post = post_query.first()
     if(post_query.first() == None):
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"we didn't find {id}")
     
     if(post.owner_id != current_user.id):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform an request action")
     post_query.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
#here payload extracts all the values from the body
def update_post(id:int,updated_post: schemas.PostCreate,db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
     
     post_query = db.query(models.Post).filter(models.Post.id==id)
     post= post_query.first()
    
     if(post  == None):
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"we didn't find {id}")
     if(post.owner_id != current_user.id):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform an request action")
     post_query.update(updated_post.dict(),synchronize_session=False) 
     db.commit()

     return post_query.first()
