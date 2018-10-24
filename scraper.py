import pandas as pd

import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_products(page, concern, category):
    """ 
    Scrapes product information from catalogue pages

    Args:
        page : The page url to scrape
        concern : The skincare concern category
        category : The product category

    Returns:
        A dataframe with the product info for each product on the page
    """
    browser = webdriver.Chrome()
    browser.delete_all_cookies()
    browser.get(page)
    
    if browser.find_elements_by_class_name("css-1mfnet7"):
        if browser.find_element_by_class_name("css-1mfnet7").is_displayed():
            button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1mfnet7")))
            button.click()

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
    urls = [elem['href'] for elem in page_content.find_all("a", class_="css-ix8km1")]

    data = {'Brand': brands, 'Product': products, 'Price': prices, 'Category': category, 'Concern': concern, 'Link': urls}
    df = pd.DataFrame(data, columns=['Brand','Product','Price','Category','Concern','Link'])

    return df


def scrape_ingredients(target, urls):
    """ 
    Scrapes product ingredients from detail pages

    Args:
        url : List of urls to scrape
    
    Returns:
        A dataframe of product ingredients
    """
    browser = webdriver.Chrome()

    df = pd.DataFrame()

    for url in urls:
        browser.get(target + url)

        # Close modal
        if browser.find_elements_by_class_name("css-1mfnet7"):
            if browser.find_element_by_class_name("css-1mfnet7").is_displayed():
                button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1mfnet7")))
                button.click()

        browser.execute_script("window.scrollTo(0, 300);")
        time.sleep(1)

        # Open ingredients 
        if browser.find_elements_by_xpath("//span[text()='Ingredients']"):
            browser.find_element_by_xpath("//span[text()='Ingredients']").click()
            page_data = browser.page_source
            page_content = BeautifulSoup(page_data, "html.parser")
            time.sleep(1)

            # Ingredients tab
            tab = page_content.find("span", class_="css-pl1n7d", string="Ingredients")
            tabid = tab.parent.get('id')
        
            # Ingredients div
            ingredients = page_content.find("div", class_="css-1pbcsc", attrs={"aria-labelledby": tabid})
        
            # Format html
            for br in ingredients.find_all("br"):
                br.replace_with(" ")
        
            df = df.append({"Ingredients": ingredients.text}, ignore_index=True)
        
        # No ingredients
        else:
            df = df.append({"Ingredients": "N/A"}, ignore_index=True)
    
    return df