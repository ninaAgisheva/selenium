import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


LINK = 'http://localhost/litecart/admin/login.php'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(2)

    authorize(browser)

    yield browser  # тут урпавление передается тесту

    browser.quit()


def authorize(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button_login = browser.find_element_by_name('login').click()


def open_catalot(browser):
    general_menu = browser.find_element_by_id('box-apps-menu')
    first_range_menu_elements_collection = general_menu.find_elements(by=By.ID, value='app-')
    first_range_menu_elements_collection[1].click()

def button_new_produkt(browser):
    list_button = browser.find_element_by_class_name('button')
    button_product = list_button[1]
    link = button_product.find_element_by_tag_name('a')
    link.click()

