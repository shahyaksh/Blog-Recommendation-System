import selenium as sc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests as re
import os
import time
print("enter: ")
tag=input()
url = f'https://techcrunch.com/category/{tag}'
driver = webdriver.Firefox()
driver.get(url)
time.sleep(5)
source = driver.page_source
soup = BeautifulSoup(source, 'html.parser')
blogs=[]
blog={}
driver.delete_all_cookies()

# for i in range(0,2):
button=driver.find_element(By.CLASS_NAME,'load-more')
button.click()
time.sleep(5)
# time.sleep(3)
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 1
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # print(topics)
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
for article in soup.find_all('article', class_='post-block post-block--image post-block--unread'):
    blog['title']=article.find('h2',class_='post-block__title').text
    blog['link']='https://techcrunch.com'+article.find('h2',class_='post-block__title').find('a')['href']
    blog['author']=article.find('span', class_='river-byline__authors').find('span').find('a').text
    blog['content']=article.find('div',class_='post-block__content').text
    images=article.find('figure',class_='post-block__media').find('picture').find_all('source')
    blog['img'] =images[2]['srcset']
    blogs.append(blog)
    blog={}

print(blogs)
print(len(blogs))
