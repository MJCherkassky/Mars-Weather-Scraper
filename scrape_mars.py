#Import dependencies and create html filepath
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

#Set Executable Path & identify url path
executable_path = {"executable_path": "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

# Create functions for each part of the Jupyter Notebook
def scrape_NASA(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html= browser.html
    soup = bs(html, 'html.parser')
    print(soup.prettify())
    first_article = soup.select_one('ul.item_list li.slide')
    news_title = first_article.find('div', class_='content_title').text
    news_p = first_article.find('div', class_='article_teaser_body').text

    return news_title, news_p

def scrape_JPL_img(browser):
    iurl= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(iurl)
    full_image_button = browser.find_by_id('full_image', )
    full_image_button.click()
    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()
    html = browser.html
    image_souped = bs(html, 'html.parser')
    image_url = image_souped.select_one('figure.lede a img').get('src')
    image_url
    direct_image_url = f"https://www.jpl.nasa.gov{image_url}"
    
    return direct_image_url

def scrape_twitter(browser):
    wurl= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(wurl)
    twitter_response = requests.get(wurl)
    weather_soup = bs(twitter_response.text, 'html.parser')
    twitter_text = weather_soup.find_all('div', class_='js-tweet-text-container')[0].text
    
    return twitter_text

def scrape_Mars_facts(browser):
    furl = 'https://space-facts.com/mars/'
    fact_tables = pd.read_html(furl)
    mars_tables = fact_tables[0]
    mars_tables.columns = ["Description","Value"]
    mars_tables.set_index('Description', inplace=True)
    mars_tables.to_html()

    return mars_tables

def scrape_hemi_images(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        hemisphere["Title"] = browser.find_by_css("h2.title").text
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["Image URL"] = sample_element["href"]     
        hemisphere_image_urls.append(hemisphere)   
        browser.back()

    return hemisphere_image_urls

def scrape_all():
    executable_path = {"executable_path": "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_p = scrape_NASA(browser)
    direct_image_url = scrape_JPL_img(browser)
    twitter_text = scrape_twitter(browser)
    # mars_tables
    hemisephere_image_urls = scrape_hemi_images(browser)

    data = {
        "News Title":news_title,
        "News Paragraph":news_p,
        "Featured Image":direct_image_url,
        "Weather":twitter_text,
        "Hemispheres":hemisephere_image_urls
    }
    browser.quit()

if __name__=="__main__":
    print(scrape_all())