from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    ###NASA Mars News

    # Visit https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Get latest headline
    content = soup.find('div', class_='content_title')
    news_title = content.text

    # Get latest paragraph text
    para = soup.find('div',class_='article_teaser_body')
    news_p = para.text

    ####JPL Mars Space Images - Featured Image
    #visit https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    browser = init_browser()

    images_url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url) 

    time.sleep(1)

    #click on full image
    button = browser.find_by_id('full_image').first
    button.click() 
    #click on more info
    browser.click_link_by_partial_text('more info')

    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    #fetch featured image
    image_url = image_soup.find("figure",class_="lede").\
                 find("a")['href']
    base_url = "https://www.jpl.nasa.gov"

    featured_image_url = base_url + image_url

    ### Mars Weather
    browser = init_browser()

    tweet_url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)

    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    mars_weather_text = weather_soup.find("p", class_="tweet-text").get_text()

    mars_weather_text = mars_weather_text.strip("Papic.twitter.com/8235o0ln3B")

    #removing trailing newlines
    mars_weather_list = mars_weather_text.splitlines()
    separator = " "
    mars_weather = separator.join(mars_weather_list)

    ### Mars Facts

    fact_url = 'https://space-facts.com/mars/'

    table = pd.read_html(fact_url)
    mars_facts_df= table[0]

    mars_facts_df.columns = ['Parameter','Values']
    mars_facts_df = mars_facts_df.set_index("Parameter")

    facts_table_html = mars_facts_df.to_html()
    facts_list = facts_table_html.splitlines()
    separator = ""
    facts_table_html = separator.join(facts_list)


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_fact_table": facts_table_html,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
