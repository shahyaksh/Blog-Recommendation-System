from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import mysql.connector as SqlConnector
import time
from datetime import datetime
from pytz import timezone

while True:
    try:
        mydb = SqlConnector.connect(host="blog-recommedation-system.cu9zz7jlsnla.ap-south-1.rds.amazonaws.com",
                                    user="yaksh",
                                    password="Yaksh_170802", database="blog_recommendation_system")
        cursor = mydb.cursor()
        print("Connection to Database Successful")
        break
    except Exception as error:
        print("Connection to Database Failed")
        print("Error:", error)
        time.sleep(2)

app = FastAPI()
def get_blogs_in_json_format(blogs_list: list):
    blog_json = []
    for blog in blogs_list:
        cursor.execute('select author_name from author where author_id=%s', [blog[1]])
        author_name = cursor.fetchone()[0]
        blog_dict = {
            "blog_id": blog[0],
            "authors": author_name,
            "content_link": blog[4],
            "title": blog[2],
            "content": blog[3],
            "image": blog[5],
            "topic": blog[6],
            "scrape_time": blog[7]
        }
        blog_json.append(blog_dict)
        blog_dict = {}
    return blog_json

def get_blogs_to_not_consider(user_id:int):
    cursor.execute("select blog_id from likes where user_id=%s", (user_id,))
    liked_blog_list = cursor.fetchall()
    cursor.execute("select blog_id from favourites where user_id=%s", (user_id,))
    favourites_blog_list = cursor.fetchall()
    blog_list = None
    blog_id_not_to_consider_list = []
    blog_id_not_to_consider_tuple = ()
    #check for blogs which are not liked or added to favourites by the user
    if liked_blog_list is None and favourites_blog_list is None:
        blog_id_not_to_consider_tuple=None
    elif liked_blog_list is not None and favourites_blog_list is not None:
        for like_blog_id in liked_blog_list:
            blog_id_not_to_consider_list.append(like_blog_id[0])
        for fav_blog_id in favourites_blog_list:
            if fav_blog_id not in blog_id_not_to_consider_list:
                blog_id_not_to_consider_list.append(fav_blog_id[0])
    elif liked_blog_list is not None:
        for like_blog_id in liked_blog_list:
            blog_id_not_to_consider_list.append(like_blog_id[0])
    elif favourites_blog_list is not None:
        for fav_blog_id in favourites_blog_list:
            if fav_blog_id not in blog_id_not_to_consider_list:
                blog_id_not_to_consider_list.append(fav_blog_id[0])
    if blog_id_not_to_consider_tuple is not None:
        blog_id_not_to_consider_tuple = tuple(blog_id_not_to_consider_list)
    return blog_id_not_to_consider_tuple

@app.get('/')
async def root():
    return {"message": "Welcome to the Blog API Created by Yaksh Shah"}

@app.get('/blogs/{user_id}')
async def get_blogs(user_id:int):
    blog_id_not_to_consider_tuple=get_blogs_to_not_consider(user_id)
    if blog_id_not_to_consider_tuple is not None:
        cursor.execute(f""" select * from blogs where blog_id order by rand() limit 50""")
    else:
        cursor.execute(f""" select * from blogs where blog_id not in {blog_id_not_to_consider_tuple} order by rand() limit 50""")
    blogs_list = cursor.fetchall()
    blog_json = get_blogs_in_json_format(blogs_list)
    return blog_json

@app.get('/recommend/blogs/{user_id}')
async def get_recommended_blogs(user_id:int):
    pass

@app.get('/like/blogs/{user_id}')
async def get_liked_blogs(user_id:int):
    cursor.execute("select blog_id from likes where user_id=%s", (user_id,))
    liked_blogs=cursor.fetchall()
    blog_id_tuple=()
    blog_id_list=[]
    if liked_blogs is not None:
        for id in liked_blogs:
            blog_id_list.append(id[0])
        blog_id_tuple=tuple(blog_id_list)
        cursor.execute(f""" select * from blogs where blog_id in {blog_id_tuple}""")
        blogs_list = cursor.fetchall()
        blog_json = get_blogs_in_json_format(blogs_list)
        return blog_json
    else:
        return "No Liked Blogs"

@app.get('/favourites/blogs/{user_id}')
async def get_favourites_blogs(user_id:int):
    cursor.execute("select blog_id from favourites where user_id=%s", (user_id,))
    favourites_blogs=cursor.fetchall()
    blog_id_tuple=()
    blog_id_list=[]
    if favourites_blogs is not None:
        for id in favourites_blogs:
            blog_id_list.append(id[0])
        blog_id_tuple=tuple(blog_id_list)
        cursor.execute(f""" select * from blogs where blog_id in {blog_id_tuple}""")
        blogs_list = cursor.fetchall()
        blog_json = get_blogs_in_json_format(blogs_list)
        return blog_json
    else:
        return "No Blogs added to Favourites"

@app.post('/likes/user/{user_id}/blog/{blog_id}')
async def like_blog(user_id:int,blog_id:int):
    curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    datetime_obj = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')
    cursor.execute("""insert into likes(user_id,blog_id,date_created)values(%s,%s,%s)""",[user_id,blog_id,datetime_obj])
    mydb.commit()
    return "Inserted"

@app.delete('/deletelike/user/{user_id}/blog/{blog_id}')
async def unlike_blog(user_id:int,blog_id:int):
    cursor.execute(""" delete from likes where user_id=%s and blog_id=%s""",(user_id,blog_id))
    mydb.commit()
    return "unliked"
@app.post('/favourites/user/{user_id}/blog/{blog_id}')
async def add_blog_to_favourites(user_id:int,blog_id:int):
    cursor.execute("""insert into favourites(user_id,blog_id)values(%s,%s)""",[user_id,blog_id])
    mydb.commit()
    return "Added to Favourites"

@app.delete('/removefromfavourites/user/{user_id}/blog/{blog_id}')
async def remove_blog_from_favourites(user_id:int,blog_id:int):
    cursor.execute(""" delete from favourites where user_id=%s and blog_id=%s""",(user_id,blog_id))
    mydb.commit()
    return "Removed from Favourites"

#uvicorn app.main:app --reload