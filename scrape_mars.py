import requests
from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

def scrape():
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(mars_news_url)

    soup = BeautifulSoup(browser.html, 'html.parser')
    news_list = soup.find('ul', class_='item_list')
    latest_news_item = news_list.find('li')
    latest_news_title = latest_news_item.find('div', class_='content_title').find('a').text
    latest_teaser = latest_news_item.find('div', class_='article_teaser_body').text

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    browser.click_link_by_id("full_image")
    browser.is_element_present_by_css('.fancybox-image')
    soup = BeautifulSoup(browser.html, 'html.parser')
    featured_image = soup.find('img', class_='fancybox-image')
    parsed_url = urlparse(browser.url)
    featured_image_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{featured_image.attrs['src']}"

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    mars_weather = soup.find('li', class_='js-stream-item').find('p', class_='tweet-text').contents[0]

    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    mars_dfs = pd.read_html(browser.html)
    mars_df = mars_dfs[0]
    mars_facts_table = mars_df.to_html()

    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    hemisphere_sections = soup.find('div', class_='results').findAll('div', class_='item')
    hemisphere_titles = [hemisphere_section.find('h3').text for hemisphere_section in hemisphere_sections]

    hemisphere_image_urls = []
    for hemisphere_title in hemisphere_titles:
        browser.click_link_by_partial_text(hemisphere_title)
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_url = soup.find('div', class_='downloads').find('a').attrs['href']
        hemisphere_image_urls.append({
            "title": hemisphere_title[:-9], # remove Enhanced
            "image_url": image_url
        })
        browser.back()
        
    return {
        "hemisphere_image_urls": hemisphere_image_urls,
        "mars_facts_table": mars_facts_table,
        "mars_weather": mars_weather,
        "featured_image_url": featured_image_url,
        "news_title": latest_news_title,
        "news_p": latest_teaser
    }

