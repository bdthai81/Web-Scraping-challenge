# Load Modules
from splinter import Browser
import pandas as pd
import time

def init_browser():
        # Launch splinter browser
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        return Browser('chrome', **executable_path, headless=False)

def scrape():
        browser = init_browser()
        mars_data = {}
        hemispheres_data = []

        # NASA Mars News
        # URL of Mars news page to be scraped
        url = 'https://mars.nasa.gov/news'
        browser.visit(url)
        time.sleep(1)
        # Find slides and save the first's info
        first_news = browser.find_by_css(f'li[class="slide"]').first
        news_title = first_news.find_by_css(f'div[class="content_title"]').text
        news_p = first_news.find_by_css(f'div[class="article_teaser_body"]').text
        mars_data["news_title"] = news_title
        mars_data["news_p"] = news_p

        # JPL Mars Space Images - Featured Image
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        time.sleep(1)
        # find the image url for the current Featured Mars Image and assign the url string
        featured_img = browser.find_by_css(f'a[class="button fancybox"]').first
        featured_image_url = "https://www.jpl.nasa.gov/" + featured_img['data-fancybox-href']
        mars_data["featured_image_url"] = featured_image_url

        # Mars Weather
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        time.sleep(1)
        # Save the tweet text for the weather report
        mars_weather_first = browser.find_by_css(f'div[class="js-tweet-text-container"]').first
        # Split data and keep only the temperature data
        mars_weather = mars_weather_first.find_by_tag('p').text.split('\n')[0]
        mars_data["mars_weather"] = mars_weather

        # Mars Facts
        url = 'http://space-facts.com/mars/'
        # Get tables from url with pandas
        tables = pd.read_html(url)
        time.sleep(1)
        # Take the first table DataFrame and name the columns
        df = tables[0]
        df.columns = ['Fact', 'Value']
        # Convert the DataFrame table to html
        html_table = df.to_html(index=False)
        html_table = html_table.replace('\n', '')
        mars_data["html_table"] = html_table

        # Mars Hemispheres
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(1)
        # Use a Python dictionary to store the data using the keys img_url and title
        items = browser.find_by_css(f'div[class="item"]')
        # Create temp list to store hemisphere title and url
        temp_hemisphere_list = []
        # store the titles and hemisphere urls into list
        for item in items:
                title = item.find_by_tag('h3').text
                hemisphere_url = item.find_by_tag('a')['href']
                temp_hemisphere_list.append({hemisphere_url:title})    
        # Parse thru the hemisphere and store the titles and hemisphere urls into list
        for hemisphere in temp_hemisphere_list:
                for key, value in hemisphere.items(): 
                        browser.visit(key)
                        download = browser.find_by_css(f'div[class="downloads"]').first
                        orginal_anchor = download.find_by_text('Sample')
                        img_url  = orginal_anchor["href"]
                        hemispheres_data.append({"name": value, "img_url": img_url})

        mars_data["hemispheres"] = hemispheres_data
        return mars_data

