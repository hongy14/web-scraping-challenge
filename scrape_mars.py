from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import re
import pandas as pd

url_1 = "https://mars.nasa.gov/news/"
url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
url_3 = "https://twitter.com/marswxreport?lang=en"
url_4 = "https://space-facts.com/mars/"
url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

def scrape( ):
    executable_path = {"executable_path": "C:\\Users\\hongy\\Desktop\\chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    
    article_title, paragraph = mars_news(browser)

    data = {
        "news_title" : article_title,
        "news_paragraph" : paragraph,
        "feature_image" : featured_image(browser),
        "hemisphere" : hemisphere(browser),
        "weather" : weather(browser),
        "mars_facts" : mars_facts(browser)
    }

    return data

def mars_news(browser):
    #Scraping the article title and paragraph
    browser.visit(url_1)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    article_title = soup.find_all('div', class_='content_title')[1].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    return article_title, paragraph

def featured_image(browser):
    #Scraping the main image url
    browser.visit(url_2)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")
    feature_image = browser.find_by_id('full_image')
    feature_image.click()

    large_image = browser.find_by_text('more info     ')
    large_image.click()
    html = browser.html
    soup = bs(html, "html.parser")
    url = soup.find_all('img', class_='main_image')

    for url in url:
        new_url = url['src']
    featured_image_url = f'https://www.jpl.nasa.gov{new_url}'

    return featured_image_url

def weather(browser):
    #Scraping the twitter account
    browser.visit(url_3)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    pattern = re.compile(r'InSight sol')
    mars_weather = soup.find('span', text=pattern).text
    mars_weather = mars_weather.replace('\n', ' ')

    return mars_weather

def mars_facts(browser):
    #Scraping the facts table
    browser.visit(url_4)
    tables = pd.read_html(url_4)
    mars_facts = tables[0]
    mars_facts.columns=['Description', 'Value']
    mars_facts = mars_facts.set_index("Description")
    html_table = mars_facts.to_html()
    html_table = html_table.replace('\n', '')
    
    return html_table

def hemisphere(browser):
    #Scraping the hemisphere images
    browser.visit(url_5)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    image_title = soup.find_all('h3')
    image_1 = image_title[0].text
    image_2 = image_title[1].text
    image_3 = image_title[2].text
    image_4 = image_title[3].text
    image_list = [image_1, image_2, image_3, image_4]

    image_urls = [ ]

    for i in range (4):
        browser.find_by_css("a.product-item h3")[i].click()
        sample_button = browser.find_by_text('Sample').first
        image_urls.append(sample_button['href'])
        browser.back()
    
    image_1_dict = {
        "image_url": image_urls[0],
        "image_title" : image_list[0]
    }
    image_2_dict = {
        "image_url": image_urls[1],
        "image_title" : image_list[1]
    }
    image_3_dict = {
        "image_url": image_urls[2],
        "image_title" : image_list[2]
    }
    image_4_dict = {
        "image_url": image_urls[3],
        "image_title" : image_list[3]
    }

    image_list = [image_1_dict, image_2_dict, image_3_dict, image_4_dict]

    return image_list

if __name__ == "__main__":
    print(scrape())