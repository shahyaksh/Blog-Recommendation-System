from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector as SqlConnector
import pandas as pd
import time
import os
import pathlib
from datetime import datetime
from pytz import timezone
from Recommend_Blogs.Using_Cosine_Similarity import pre_process_text
import random

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

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_like_counts(blog_id:int):
    cursor.execute(""" select * from likes where blog_id=%s""",[blog_id])
    likes=cursor.fetchall()
    counts = len(likes)
    return counts

def get_blogs_in_json_format(blogs_list: list,for_recommendation:bool=False):
    blog_json = []
    if for_recommendation==True:
        for blog in blogs_list:
            blog_dict = {
                "blog_id": blog[0],
                "content": blog[1],
                "topic": blog[2]
            }
            blog_json.append(blog_dict)
            blog_dict = {}
        return blog_json
    else:
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
                "like_count":get_like_counts(blog[0]),
                "scrape_time": blog[7]

            }
            blog_json.append(blog_dict)
            blog_dict = {}
        return blog_json

def get_blogs_not_to_consider(user_id:int):

    # get all blogs liked by the user
    cursor.execute("select blog_id from likes where user_id=%s", (user_id,))
    liked_blog_list = cursor.fetchall()
    #get all blogs that are added to favourites by the user
    cursor.execute("select blog_id from favourites where user_id=%s", (user_id,))
    favourites_blog_list = cursor.fetchall()

    blog_id_not_to_consider_list = []
    blog_id_not_to_consider_tuple = ()
    #check for blogs which are liked or added to favourites by the user and form a tuple
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
    if blog_id_not_to_consider_list is not None:
        blog_id_not_to_consider_tuple = tuple(blog_id_not_to_consider_list)
    return blog_id_not_to_consider_tuple

def add_user_ratings(user_id:int,blog_id:int):
    cursor.execute("""select * from ratings where blog_id=%s and user_id=%s""", [blog_id, user_id])
    if cursor.fetchone():
        return "Already exist"
    else:
        curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
        datetime_obj = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')
        cursor.execute("""insert into ratings(user_id,blog_id,rating,timestamp)values(%s,%s,%s,%s)""",
                       [user_id, blog_id, 0.5, datetime_obj])
        mydb.commit()
        return "seen"


def update_user_rating(user_id:int):
    curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    datetime_obj = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')

    cursor.execute(""" update ratings set rating=%s,timestamp=%s where user_id=%s and blog_id in
                        (select * from (select likes.blog_id from likes inner join ratings on 
                        likes.user_id = ratings.user_id and likes.blog_id=ratings.blog_id) tb1tmp)""",
                   [2,datetime_obj,user_id])
    mydb.commit()

    cursor.execute(""" update ratings set rating=%s,timestamp=%s where user_id=%s and blog_id in
                      (select * from (select favourites.blog_id from favourites inner join ratings on 
                    favourites.user_id = ratings.user_id and favourites.blog_id=ratings.blog_id) tb1tmp)""",
                   [3.5,datetime_obj,user_id])
    mydb.commit()

    cursor.execute(""" update ratings set rating=%s,timestamp=%s where user_id=%s and blog_id in 
                        (select * from (select favourites.blog_id from favourites inner join likes on 
                        likes.user_id=favourites.user_id and likes.blog_id=favourites.blog_id)tb1tmp)""",
                        [5,datetime_obj,user_id])
    mydb.commit()
def get_user_ratings_in_json_format(ratings_list:list):
    ratings_json = []
    for rating in ratings_list:
        rating_dict = {
            "user_id": rating[0],
            "blog_id": rating[1],
            "rating": rating[2],
        }
        ratings_json.append(rating_dict)
        rating_dict = {}
    return ratings_json

def get_blogs_for_recommendation(recommended_blogs:tuple):
    cursor.execute(f'select * from blogs where blog_id in {recommended_blogs}')
    blogs_list = cursor.fetchall()
    blogs_json = get_blogs_in_json_format(blogs_list)
    return blogs_json

#Blog Ratings
path = os.path.join(pathlib.Path(__file__).parent,('blog_ratings_V4.csv'))
ratings_df = pd.read_csv(path)
# This logic checks whether new blogs are added to the database if yes then it will add those blogs to the csv file
cursor.execute("select max(blog_id) from blogs")
max_id = cursor.fetchone()
data_file = os.path.abspath("Recommend_Blogs/blog_data.csv")
blog_data = pd.read_csv(data_file)
last_blog_id=blog_data['blog_id'].iloc[-1]

if max_id[0] > last_blog_id:
    cursor.execute(f'select blog_id,blog_content,topic from blogs where blog_id > {last_blog_id}')
    blogs_list = cursor.fetchall()
    blogs_json = get_blogs_in_json_format(blogs_list, True)
    blog_data_2 = pd.DataFrame(blogs_json)
    blog_data_2.columns = ['blog_id', 'content', 'topic']
    blog_data_2['clean_blog_content'] = blog_data_2['content'].apply(
        lambda x: pre_process_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=None))
    blog_data = pd.concat([blog_data, blog_data_2], ignore_index=True)
    blog_data.to_csv(data_file, index=False)

