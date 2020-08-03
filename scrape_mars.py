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
    executable_path = {"executable_path": "./chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []
    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        # Find element to navigate to each hemisphere page
        browser.find_by_css("a.product-item h3")[item].click()
        # Get hemisphere name text
        hemisphere["Title"] = browser.find_by_css("h2.title").text
        # Extract href tag from Sample jpg
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["Image URL"] = sample_element["href"]
        # Append info dictionary to above list
        hemisphere_image_urls.append(hemisphere)
        # Return to main Mars Hemisphere page to restart the for loop at the top
        browser.back()

    scrape_data_dict= {
    "News Title": news_title,
    "News Paragraph": news_p,
    "Image": direct_image_url,
    "Tweet":first_tweet,
    "Mars Facts": mars_tables,
    "Hemisphere Image URL's":hemisphere_image_urls
    }

    return scrape_data_dict
