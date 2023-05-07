import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Set up the Firefox web driver
driver = webdriver.Firefox()

# Navigate to the website
driver.get("https://thenextweb.com/topic/artificial-intelligence")

# Scroll down to the bottom of the page
for i in range(0,2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    # Click the "Load More" button
    load_more_button = driver.find_element("id",'articleListButton')
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
articles = soup.find_all("article", class_="c-listArticle")
for article in articles:
    div = article.find("div", class_="c-listArticle__text")
    blog['title'] = div.find("h4", class_="c-listArticle_heading").find("a", class_="title_link").text
    link = div.find("h4", class_="c-listArticle__heading").find("a")["href"]
    blog['final link'] = "https://thenextweb.com" + link
    blog['author'] = div.find("a", class_="c-meta__link").text
    # blog['img link'] = article.find("figure",class_="c-listArticle__image").find('a')['href']
    blogs.append(blog)
    blog = {}

# Print the list of dictionaries and the number of articles scraped
print(f"Number of articles scraped: {len(blogs)}")
print(blogs)

# Quit the web driver
driver.quit()