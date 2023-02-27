import selenium as sc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import requests as re
from def_image import getImage
import os
import time
from pytz import timezone
from AddBlogToDB.insert_blog import get_author_id,insert_blog_in_db

os.environ['PATH']+=r"C:/SeleniumDrivers"
driver = webdriver.Firefox()

time.sleep(2)


def web_scrape(tag:str):
    trending_url = f'https://medium.com/tag/{tag}'
    latest_url = f'https://medium.com/tag/{tag}/latest'
    driver.get(trending_url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    SCROLL_PAUSE_TIME = 1
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    source_page = driver.page_source
    soup = BeautifulSoup(source_page, 'html.parser')
    blogs=[]
    blog={}
    All_Articals = soup.find_all('article')
    curr_time=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    for article in All_Articals:
        source=article.find('div',recursive=False).find_all('a')
        blog['blog_website_name'] = 'medium'
        blog['author']=source[0].find('img')['alt']
        blog['author_id'] = get_author_id(blog['author'], blog['blog_website_name'])
        blog['blog_link']='https://medium.com'+source[3]['href']
        content_info=source[3].find_all('div')
        if(content_info==[]):
            content_info=source[4].find_all('div')
        blog['blog_title']=content_info[0].text
        blog['blog_content']=content_info[1].text
        if source[len(source)-4].find('img')==None:
        # Get default image from def_image package
            blog['blog_img']=getImage.get_image(tag)
        else:
            blog['blog_img']=source[len(source)-4].find('img')['src']

        blog['blog_topic']=tag
        blog['timestamp']=curr_time
        blogs.append(blog)
        res=insert_blog_in_db(blog)
        blog={}
    return blogs

if __name__=="__main__":
    blogs=web_scrape('data-science')