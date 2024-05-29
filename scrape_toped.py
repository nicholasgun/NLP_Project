import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# link
product_link = 'https://www.tokopedia.com/putragroup/resmi-iphone-11-64gb-128gb-garansi-indo-1-tahun-64-128-gb-64gb-black-promo-f27ca?extParam=cmp%3D1%26ivf%3Dfalse&src=topads'

# open product link
driver = webdriver.Chrome()
driver.get(product_link)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# go to review section
all_review = soup.find_all('a', attrs={'data-testid' : 'btnViewAllFeedback'})
link_all_review = all_review[0]['href']
link_all_review = 'https://www.tokopedia.com' + link_all_review
driver.get(link_all_review)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# get number of pages
total_pages = soup.find_all('button', attrs={'class' : 'css-bugrro-unf-pagination-item'})
num_page = 0
for page in total_pages :
    if not page.text.isdigit() :
        continue
    if int(page.text) > num_page :
        num_page = int(page.text)

# get all review
reviews = []
for i in range (0, num_page-1):
    toped_reviews = soup.find_all('article', attrs={'class' : 'css-72zbc4'})
    for review in toped_reviews:
        # blank review checking
        if review.find('span', attrs={'data-testid' : 'lblItemUlasan'}) is not None : 
            text_review = review.find('span', attrs={'data-testid' : 'lblItemUlasan'}).text
            reviews.append(text_review)
    time.sleep(3)
    # click next page  
    try :
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Laman berikutnya"]').click()
    except :
        break
    time.sleep(3)
