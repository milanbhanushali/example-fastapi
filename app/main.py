#region Import Libraries
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#endregion Import Libraries

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

          
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
          

#region path operation or route
@app.get("/")
def root():
    return{"message" : "welcome to my api"}
#endregion path operation or route 






#region in this for execution we are writing Queries


# @app.get("/posts")
# def get_post():
#      cursor.execute("""SELECT * FROM posts""")
#      posts = cursor.fetchall()
#      print(posts)
#      return{"data" : posts }

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# #here payload extracts all the values from the body
# def create_post(post: Post):
#      cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""" , (post.title,post.content,post.published))
#      new_post = cursor.fetchone()
#      conn.commit()
#      return{"data" : new_post}


# @app.get("/posts/{id}")
# def get_post(id : int):
#      cursor.execute("""SELECT * FROM posts WHERE id= %s""" ,(str(id)))
#      post = cursor.fetchone()     
#      if not post:
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
#         #   response.status_code = status.HTTP_404_NOT_FOUND
#         #   return {"message" : f"post with id: {id} was not found"}
#      return {"post_detail" :post}

# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#      cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,str(id))
#      deleted_post = cursor.fetchone()
#      print(deleted_post)
#      conn.commit()
#      if(deleted_post == None):
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"we didn't find {id}")
#      return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# #here payload extracts all the values from the body
# def update_post(id:int,post: Post):
#      cursor.execute(""" UPDATE posts SET  title = %s , content = %s , published = %s WHERE id = %s RETURNING *""" , (post.title,post.content,post.published,str(id)))
#      updated_post = cursor.fetchone()
#      conn.commit()
    
#      if(updated_post  == None):
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"we didn't find {id}")

#      return{"data" : updated_post}

#endregion in this for execution we are writing Queries