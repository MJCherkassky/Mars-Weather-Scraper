#Import dependencies and create html filepath
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from twitter_scraper import get_tweets

# Create functions from Jupyter Notebook work
def scrape():
    ############ NASA MARS NEWS ############

    #Set Executable Path & identify url path
    executable_path = {"executable_path": "./chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Parse webpage
    html= browser.html
    soup = bs(html, 'html.parser')
    first_article = soup.select_one('ul.item_list li.slide')
    news_title = first_article.find('div', class_='content_title').text
    news_p = first_article.find('div', class_='article_teaser_body').text

    ############ JPL MARS FEATURED IMAGE ############
    #Set Executable Path & identify URL path
    executable_path = {"executable_path": "./chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    iurl= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(iurl)

    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()
    more_info_element = browser.find_link_by_partial_text('more info')
    more_info_element.click()
    html = browser.html
    image_souped = bs(html, 'html.parser')
    image_url = image_souped.select_one('figure.lede a img').get('src')
    direct_image_url = f"https://www.jpl.nasa.gov{image_url}"

    ############# MARS TWITTER WEATHER ############
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html_weather=browser.html
    soup=bs(html_weather, 'html.parser')
    tweets=[]
    for tweet in get_tweets('@MarsWxReport', pages=1):
        tw=tweet['text']
        tweets.append(tw)
    first_tweet = tweets[0]

    ############ MARS FACTS ############
    furl = 'https://space-facts.com/mars/'
    fact_tables = pd.read_html(furl)
    mars_tables = fact_tables[0]
    mars_tables.columns = ["Description","Value"]
    mars_tables.set_index('Description', inplace=True)
    mars_tables.to_html()

    ############ MARS HEMISPHERES ############
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
    ]

    scrape_data_dict= {
    "News Title": news_title,
    "News Paragraph": news_p,
    "Image": direct_image_url,
    "Tweet":first_tweet,
    "Mars Facts": mars_tables,
    "Hemisphere Image URL's":hemisphere_image_urls
    }
    browser.quit()
    return scrape_data_dict

if __name__ == "__main__":
    print(scrape())
