import pandas as pd
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def scrape_products(page, concern, category):
    """ Returns a dataframe containing info for each product scraped off the page

        page (string) : The page url to scrape
        concern (string) : The skincare concern category
        category (string) : The product category
    """
    browser = webdriver.Chrome()
    browser.get(page)
    
    if len(browser.find_elements_by_class_name("css-1mfnet7")) > 0:
        browser.find_element_by_class_name("css-1mfnet7").click()

    page_height = browser.execute_script("return document.body.scrollHeight")
    scroll = 0

    # Scroll to load items
    while scroll < page_height:

        scroll += 150

        if scroll > page_height:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            break

        browser.execute_script("window.scrollTo(0, " + str(scroll) + ");")
        time.sleep(3)

    # Fetch content
    page_data = browser.page_source
    page_content = BeautifulSoup(page_data, "html.parser")

    # Brand, Product Name, Price, Link
    brands = [brand.text for brand in page_content.find_all("span", class_="css-ktoumz")]
    products = [product.text for product in page_content.find_all("span", attrs={"data-at": "sku_item_name"})]
    prices = [price.text for price in page_content.find_all("span", attrs={"data-at": "sku_item_price_list"})]
    links = [elem['href'] for elem in page_content.find_all("a", class_="css-ix8km1")]

    data = {'Brand': brands, 'Product': products, 'Price': prices, 'Category': category, 'Concern': concern, 'Link': links}
    df = pd.DataFrame(data, columns=['Brand','Product','Price','Category','Concern','Link'])

    return df

# concern = "Acne"
# page = 'https://www.sephora.com/ca/en/shop/acne-products-acne-cream?pageSize=300'
# category = "Treatment"
# df = scrape_products(page, concern, category)
# df.to_csv("acne_treatments.csv", encoding='utf-8')