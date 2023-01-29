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
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
authors = []
topics = []
content_link=[]
content=[]
title=[]

source_page = driver.page_source
# articles = driver.find_element('article').text
soup = BeautifulSoup(source_page, 'html.parser')
All_Articals = soup.find_all('article')
for article in All_Articals:
    authors.append(article.find('a', class_="ae af ag ah ai aj ak al am an ao ap aq ar as").find('p').text)
    content_link.append('https://medium.com'+article.find('div',class_="l",recursive=False).find('a')['href'])
    content_info=article.find('div',class_="l cj jr").find_all('div')
    # content_info = article.find('div', class_="l",recursive=False).find_all('div')
    title.append(content_info[0].text)
    content.append(content_info[1].text)
                   # [len(content_info[0].text):])



    # topics.append(article.select('h2.bd.ij.kc.kd.ke.kf.eo.kg.kh.ki.kj.es.kk.kl.km.kn.ew.ko.kp.kq.kr.fa.ks.kt.ku.kv.fe.ff.fg.fh.fj.fk.bi'))
print(len(authors))
print(content_link)
print(title)
print(content)