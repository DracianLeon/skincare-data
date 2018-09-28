import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Selenium to scroll 
browser = webdriver.Chrome()

# Acne/Blemish Products
page_link = 'https://www.sephora.com/ca/en/shop/acne-treatment-blemish-remover?pageSize=300'

browser.get(page_link)
browser.find_element_by_class_name("css-1mfnet7").click()

page_height = browser.execute_script("return document.body.scrollHeight")
scroll = 0

while scroll < page_height:

    scroll += 150

    if scroll > page_height:
         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
         break

    # Scroll down in increments
    browser.execute_script("window.scrollTo(0, " + str(scroll) + ");")
    
    # Wait to load page
    time.sleep(1)

page_data = browser.page_source

# Fetch content
page_content = BeautifulSoup(page_data, "html.parser")

# Brand, Product Name, Price
brands = page_content.find_all("span", attrs={"data-at": "sku_brand_name"})
products = page_content.find_all("span", attrs={"data-at": "sku_item_name"})

# Grab href for product -> for each product navigate to page and get ingredients?




