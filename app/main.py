from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from itsdangerous import NoneAlgorithm
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                user='postgres', password='Gaming.004', cursor_factory=RealDictCursor)
        cursor = conn.cursor
        print('Database connection was succesfull!')
        break
    except Exception as error:
        print('Connection to database was failed!')
        print("Error :", error)
        time.sleep(2)

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
{"title":"favourite food", "content":"I like pizza", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict= post.dict()
    post_dict['id']=randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} wasnot found")
    return {"post detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"the post with id:{id} doesn't exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"the post with id:{id} doesn't exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
