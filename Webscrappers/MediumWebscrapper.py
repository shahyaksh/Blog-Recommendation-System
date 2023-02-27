import selenium as sc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests as re
import os
import time
os.environ['PATH']+=r"C:/SeleniumDrivers"
driver = webdriver.Firefox()
tag=input()
trending_url = f'https://medium.com/tag/{tag}'
latest_url = f'https://medium.com/tag/{tag}/latest'
driver.get(trending_url)
time.sleep(2)
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 3
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
blogs=[]
blog={}

source_page = driver.page_source
soup = BeautifulSoup(source_page, 'html.parser')
All_Articals = soup.find_all('article')

for article in All_Articals:
    source=article.find('div',recursive=False).find_all('a')
    blog['authors']=source[0].find('img')['alt']
    blog['content_link']='https://medium.com'+source[2]['href']
    content_info=source[3].find_all('div')
    if(content_info==[]):
        content_info=source[4].find_all('div')
    blog['title']=content_info[0].text
    blog['content']=content_info[1].text
    # blog['image']=source[len(source)-3].find('img')['src']
    blogs.append(blog)
    print(source)

print(len(blogs))
print(blogs)