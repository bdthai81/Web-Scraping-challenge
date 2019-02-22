# Load Modules
from splinter import Browser
import pandas as pd

# Launch splinter browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# NASA Mars News
# URL of Mars news page to be scraped
url = 'https://mars.nasa.gov/news'
browser.visit(url)
# Find slides and save the first's info
first_news = browser.find_by_css(f'li[class="slide"]').first
news_title = first_news.find_by_css(f'div[class="content_title"]').text
news_p = first_news.find_by_css(f'div[class="article_teaser_body"]').text
print(news_title, '\n', news_p)


# JPL Mars Space Images - Featured Image
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
# find the image url for the current Featured Mars Image and assign the url string
featured_img = browser.find_by_css(f'a[class="button fancybox"]').first
featured_image_url = "https://www.jpl.nasa.gov/" + featured_img['data-fancybox-href']
featured_image_url

# Mars Weather
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
# Save the tweet text for the weather report
mars_weather_first = browser.find_by_css(f'div[class="js-tweet-text-container"]').first
# Split data and keep only the temperature data
mars_weather = mars_weather_first.find_by_tag('p').text.split('\n')[0]

# Mars Facts
url = 'http://space-facts.com/mars/'
# Get tables from url with pandas
tables = pd.read_html(url)
# Take the first table DataFrame and name the columns
df = tables[0]
df.columns = ['Fact', 'Value']
# Convert the DataFrame table to html
html_table = df.to_html()
html_table = html_table.replace('\n', '')
html_table

# Mars Hemispheres
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
# Use a Python dictionary to store the data using the keys img_url and title
items = browser.find_by_css(f'div[class="item"]')
# Create temp list to store hemisphere title and url
temp_hemisphere_list = []
# store the titles and hemisphere urls into list
for item in items:
    title = item.find_by_tag('h3').text
    hemisphere_url = item.find_by_tag('a')['href']
    temp_hemisphere_list.append({hemisphere_url:title})    
# Create list to store hempishere title and image url
hemisphere_list = []
# Parse thru the hemisphere and store the titles and hemisphere urls into list
for hemisphere in temp_hemisphere_list:
    for key, value in hemisphere.items(): 
        browser.visit(key)
        download = browser.find_by_css(f'div[class="downloads"]').first
        orginal_anchor = download.find_by_text('Original')
        img_url  = orginal_anchor["href"]
        hemisphere_list.append({img_url:value})

hemisphere_list

