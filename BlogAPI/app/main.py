from app import *
from Recommend_Blogs import Using_Cosine_Similarity


@app.get('/')
async def root():
    return {"message": "Welcome to the Blog API Created by Yaksh Shah"}

@app.post('/register/name/{user_name}/email/{user_email}')
async def register_user(user_name:str,user_email:str):
    user_query = ''' insert into user_profile(user_name,user_email,user_pic)
                        values(%s,%s,%s) '''
    user_info = (user_name,user_email,'default_profile_pic.jpg')
    # execute the query
    cursor.execute(user_query, user_info)
    mydb.commit()
    return "User Registeration Completed"

@app.get('/login/email/{user_email}')
async def user_login(user_email:str):
    cursor.execute(''' select user_id,user_name,user_email from user_profile 
                                    where user_email=%s''',
                   [user_email])
    resp = cursor.fetchone()
    if resp is not None:
        user_details={'user_id':resp[0],'user_name':resp[1],'user_email':resp[2],"user_res":"Found"}
        update_user_rating(user_details['user_id'])
        return user_details
    else:
        return {"user_res":"Not Found"}

@app.post('/update/name/{user_name}/id/{user_id}')
async def update_user_name(user_name:str,user_id:int):
    cursor.execute(""" update user_profile set user_name=%s where user_id=%s""",
                   [user_name, user_id])
    # execute the query
    mydb.commit()
    return "User Name Updated"

@app.post('/update/image/{user_pic}/id/{user_id}')
async def update_user_profile_pic(user_pic:str,user_id:int):
    cursor.execute(""" update user_profile set user_pic=%s where user_id=%s""",
                   [user_pic, user_id])
    # execute the query
    mydb.commit()
    return "User Profile Pic Updated"

@app.get('/name/{user_name}')
async def verify_user_name(user_name:str):
    cursor.execute(''' SELECT user_name from user_profile 
                                    where user_name=%s''', [user_name])
    result = cursor.fetchone()
    if result:
        return "unique"
    else:
        return "not unique"
    return result

@app.get('/image/id/{user_id}')
async def get_user_profile_pic(user_id:int):
    cursor.execute(""" select user_pic from user_profile where user_id=%s""", [user_id])
    resp = cursor.fetchone()
    user_img = {"user_img":resp[0]}
    return user_img

@app.get('/blogs')
async def get_blogs_for_home_before_login():
    cursor.execute(f""" select * from blogs where blog_id in(select blog_id from ratings where rating=5)
                        order by rand() limit 30""")
    blogs_list = cursor.fetchall()
    blog_json = get_blogs_in_json_format(blogs_list)
    return blog_json

@app.get('/blogs/{user_id}')
async def get_blogs_for_home_after_login(user_id:int):
    blog_id_not_to_consider_tuple=get_blogs_not_to_consider(user_id)
    if blog_id_not_to_consider_tuple is not None:
        cursor.execute(f""" select * from blogs where blog_id order by rand() limit 30""")
    else:
        cursor.execute(f""" select * from blogs where blog_id not in {blog_id_not_to_consider_tuple} order by rand() limit 30""")
    blogs_list = cursor.fetchall()
    blog_json = get_blogs_in_json_format(blogs_list)
    return blog_json

@app.get('/recommend/similar/blogs/{user_id}')
async def get_recommended_blogs_using_cosine_similarity(user_id:int):
    cursor.execute('select * from ratings where user_id=%s', [user_id])
    ratings_list = cursor.fetchall()
    ratings_json = get_user_ratings_in_json_format(ratings_list)
    if len(ratings_json) < 3:
        return []
    else:

        blogs_json=[]
        recommended_blogs = Using_Cosine_Similarity.get_similar_blog(blogs_json,ratings_json)
        print(recommended_blogs)
        recommended_blogs_json = get_blogs_for_recommendation(tuple(recommended_blogs))
        return recommended_blogs_json

@app.get('/like/blogs/{user_id}')
async def get_liked_blogs(user_id:int):
    cursor.execute("""select blog_id from likes where user_id=%s""", (user_id,))
    liked_blogs=cursor.fetchall()
    blog_id_tuple=()
    blog_id_list=[]
    blog_json=[]
    blog_list=[]
    if liked_blogs != []:
        for id in liked_blogs:
            blog_id_list.append(id[0])
        blog_id_tuple=tuple(blog_id_list)
        if len(blog_id_tuple)>1:
            cursor.execute(f""" select * from blogs where blog_id in {blog_id_tuple}""")
            blogs_list = cursor.fetchall()
            blog_json = get_blogs_in_json_format(blogs_list)
        else:
            cursor.execute(f""" select * from blogs where blog_id={blog_id_tuple[0]}""")
            blogs_list = cursor.fetchall()
            blog_json = get_blogs_in_json_format(blogs_list)

        return blog_json
    else:
        return {"res":"Not Found"}

@app.get('/favourites/blogs/{user_id}')
async def get_favourites_blogs(user_id:int):
    cursor.execute("select blog_id from favourites where user_id=%s", (user_id,))
    favourites_blogs=cursor.fetchall()
    blog_id_tuple=()
    blog_id_list=[]
    if favourites_blogs != []:
        for id in favourites_blogs:
            blog_id_list.append(id[0])
        blog_id_tuple=tuple(blog_id_list)
        if len(blog_id_tuple) > 1:
            cursor.execute(f""" select * from blogs where blog_id in {blog_id_tuple}""")
            blogs_list = cursor.fetchall()
            blog_json = get_blogs_in_json_format(blogs_list)
        else:
            cursor.execute(f""" select * from blogs where blog_id={blog_id_tuple[0]}""")
            blogs_list = cursor.fetchall()
            blog_json = get_blogs_in_json_format(blogs_list)
        return blog_json
    else:
        return {"res": "Not Found"}


@app.post('/content/seen/user/{user_id}/blog/{blog_id}')
async def seen_blog_content(user_id:int,blog_id:int):
    result=add_user_ratings(user_id,blog_id)
    return result

@app.post('/likes/user/{user_id}/blog/{blog_id}')
async def like_blog(user_id:int,blog_id:int):
    cursor.execute("""select * from likes where blog_id=%s and user_id=%s""", [blog_id, user_id])
    if cursor.fetchone():
        return "Already exist"
    else:
        curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
        datetime_obj = datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')
        cursor.execute("""insert into likes(user_id,blog_id,date_created)values(%s,%s,%s)""",[user_id,blog_id,datetime_obj])
        mydb.commit()
        add_user_ratings(user_id,blog_id)
        return "liked"

@app.delete('/deletelike/user/{user_id}/blog/{blog_id}')
async def unlike_blog(user_id:int,blog_id:int):
    cursor.execute(""" delete from likes where user_id=%s and blog_id=%s""",(user_id,blog_id))
    mydb.commit()
    return "unliked"

@app.post('/favourites/user/{user_id}/blog/{blog_id}')
async def add_blog_to_favourites(user_id:int,blog_id:int):
    cursor.execute("""select * from favourites where blog_id=%s and user_id=%s""",[blog_id,user_id])
    if cursor.fetchone():
        return "Already exist"
    else:
        cursor.execute("""insert into favourites(user_id,blog_id)values(%s,%s)""",[user_id,blog_id])
        mydb.commit()
        add_user_ratings(user_id, blog_id)
        return "Added to Favourites"

@app.delete('/removefromfavourites/user/{user_id}/blog/{blog_id}')
async def remove_blog_from_favourites(user_id:int,blog_id:int):
    cursor.execute(""" delete from favourites where user_id=%s and blog_id=%s""",(user_id,blog_id))
    mydb.commit()
    return "Removed from Favourites"


#uvicorn app.main:app --reload
