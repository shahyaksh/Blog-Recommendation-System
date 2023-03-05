# Blog-Recommendation-System
# How to install all the dependencies for our blog website

<code>pip install -r requirements.txt</code>

# To run the uvicorn server for Blog API on localhost

<code>uvicorn app.main:app --reload</code>

# To See the Documentation of the API or to Test the endpoints:
  
  <code>http://127.0.0.1:8000/docs</code>

# API Endpoints and the Description of what they do:

## 1) Endpoints with GET Requests

### a) Get_blogs_for_home_page:

-- This endpoint will return blog data in json format

<code>http://127.0.0.1:8000/blogs/6</code>
  
  
### b) Get_all_the_liked_blogs:
  
  -- This endpoint will return all the liked blogs of the user
  
  <code>http://127.0.0.1:8000/like/blogs/6</code>
  
### c) Get_favourite_blogs:
  
  -- This endpoint will return all the blogs added to favourites by the user
  
  <code>http://127.0.0.1:8000/favourites/blogs/6</code>
 
### d) Get_Recommended_blogs:
  
  -- This endpoint will provide the recommended blogs based on the user actvity which is still remaining to implement
  
  <code>http://127.0.0.1:8000//recommend/blogs/{user_id}</code>


## 2) Endpoints with POST Requests

### a) lnsert_like_to_the_blog:

-- This endpoint will insert the like into the database

<code>[http://127.0.0.1:8000/blogs/6](http://127.0.0.1:8000/likes/user/6/blog/76)</code>

### b) insert_blog_to_favourites:
  
  -- This endpoint will add the blog to user's favourite list
  
  <code>[http://127.0.0.1:8000/like/blogs/6](http://127.0.0.1:8000/favourites/user/6/blog/155)</code>
  

## 3) Endpoints with DELETE Requests

### a) Unlike_the_Blog:

-- This endpoint will unlike the blog and remove the entry from likes table

<code>http://127.0.0.1:8000/likes/user/6/blog/76</code>

### b) Remove_blog_from_favourites:
  
  -- This endpoint will remove the blog from the user's favourite list
  
  <code>http://127.0.0.1:8000/removefromfavourites/user/6/blog/20</code>
  



  
  
  
