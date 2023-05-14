import time
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


# Set up the Firefox web driver
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://venturebeat.com/category/ai/")

# Scroll down to the bottom of the page
for i in range(0,2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    # Click the "Load More" button
    load_more_button = driver.find_element("id", 'infinite-handle')
    load_more_button.click()
    time.sleep(5)

# Scroll down to the bottom of the page again to load more articles
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(5)

# Extract the title, link, and author information of the first 30 articles using BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
blogs = []
blog={}
for article in soup.find_all('article', class_='ArticleListing'):
    blog['title']=article.find('h2',class_='ArticleListing__title').find('a').text
    blog['link']=article.find('h2',class_='ArticleListing__title').find('a')['href']
    blog['author']=article.find('div', class_='ArticleListing__byline').find('a').text
    #blog['content']=article.find('div',class_='post-block__content')
    #images=article.find('figure',class_='post-block__media').find('picture').find_all('source')
    blog['img'] =article.find('img')['src']
    # tempurl = article.find('h2', class_='ArticleListing__title').find('a')['href']
    # blog['link'] = tempurl
    # response = requests.get(tempurl)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # blog['content'] = soup.find('div', class_="article-content").find("p").get_text()
    blogs.append(blog)
    blog={}

with open('blogs.csv', 'w', newline='') as csvfile:
    # Define the fieldnames for the CSV file
    fieldnames = ['title', 'link', 'author', 'img']

    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data rows
    for blog in blogs:
        writer.writerow(blog)




# Print the list of dictionaries and the number of articles scraped
print(f"Number of articles scraped: {len(blogs)}")
print(blogs)

# Quit the web driver
driver.quit()