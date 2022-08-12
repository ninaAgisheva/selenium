import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


LINK = 'http://localhost/litecart/admin/?app=countries&doc=countries'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    authorize(browser)

    yield browser  

    browser.quit()

def authorize(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button_login = browser.find_element_by_name('login').click()

def test_sort1(browser):
    browser.get(LINK)
    list_name_country(browser)

def get_list_countries(browser):
    list_countries = browser.find_element_by_class_name('dataTable')
    
    return list_countries.find_elements_by_class_name('row')

def list_name_country(browser):
    list_countries = get_list_countries(browser)
    row = get_list_countries.find_elements_by_tag_name('td')
    name_countries = row[4]
    list_sort = []

    for element in list_name_countries:

        list_sort += element

    list_sort2 = list_sort.sort()

    assert list_sort == list_sort2 





