import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


LINK = 'http://localhost/litecart/en/'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    yield browser  

    browser.quit()


def test_ducks(browser):
    browser.get(LINK)

    check_most_popular(browser)
    check_campaigns(browser)
    check_latest_products(browser)


def check_most_popular(browser):
    most_popular_list = get_most_popular(browser)

    for element in most_popular_list:
        try:
            sticker = element.find_element_by_class_name('sticker')
            time.sleep(1)
        except NoSuchElementException:
            pytest.fail()

def check_campaigns(browser):
    campaigns_list = get_campaigns(browser)

    for element in campaigns_list:
        try:
            sticker = element.find_element_by_class_name('sticker')
            time.sleep(1)
        except NoSuchElementException:
            pytest.fail()

def check_latest_products(browser):
    latest_products_list = get_latest_products(browser)

    for element in latest_products_list:
        try:
            sticker = element.find_element_by_class_name('sticker')
            time.sleep(1)
        except NoSuchElementException:
            pytest.fail()

def get_most_popular(browser):
    general_menu = browser.find_element_by_id('box-most-popular')

    return general_menu.find_elements(by=By.CLASS_NAME, value='link')


def get_campaigns(browser):
     general_menu = browser.find_element_by_id('box-campaigns')

     return general_menu.find_elements(by=By.CLASS_NAME, value='link')

def get_latest_products(browser):
     general_menu = browser.find_element_by_id('box-latest-products')

     return general_menu.find_elements(by=By.CLASS_NAME, value='link')



