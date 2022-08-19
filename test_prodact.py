import pytest
import time
import os 


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


LINK = 'http://localhost/litecart/admin/login.php'
name_product = 'test'


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


def test_filling(browser):
    press_button_catalog(browser)

    products_before = how_manu_products(browser)

    button_new_produkt(browser)
    full_fields_general(browser)
    swich_to_information(browser)
    full_fields_information(browser)
    swich_to_prices(browser)
    full_fields_price(browser)
    save_product(browser)

    products_after = how_manu_products(browser)

    if (products_after < products_before) or (products_after == products_before):
        pytest.fail()


def press_button_catalog(browser):
    general_menu = browser.find_element_by_id('box-apps-menu')
    inner_elements = general_menu.find_elements_by_tag_name('li')
    button_countries = inner_elements[1]
    button_countries.click()


def button_new_produkt(browser):
    list_button = browser.find_elements_by_class_name('button')
    button_product = list_button[1]
    link = button_product.find_element_by_tag_name('i')
    link.click()


def full_fields_general(browser):
    status = browser.find_element(By.CSS_SELECTOR, "[value='1']").click()
    name = browser.find_element_by_name('name[en]').send_keys('name_product')
    code = browser.find_element_by_name('code').send_keys('01')
    product_groups = browser.find_element(By.CSS_SELECTOR, "[value='1-1']").click()
    quantity = browser.find_element_by_name('quantity')
    quantity.clear()
    quantity.send_keys('15')
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_edd = os.path.join(current_dir, 'test.jpg')
    field_photo  = browser.find_element_by_name('new_images[]').send_keys(file_edd)
    date_valid_from = browser.find_element_by_name('date_valid_from').send_keys('17.08.2022')
    date_valid_to = browser.find_element_by_name('date_valid_to').send_keys('30.08.2022')

def swich_to_information(browser):
    tabs = browser.find_element_by_class_name('index')
    tab = tabs.find_elements_by_tag_name('li')
    information = tab[1]
    information.click()
    time.sleep(2)

def full_fields_information(browser):
    manufacturers = browser.find_element_by_xpath("//select[@name='manufacturer_id']/option[@value='1']").click()
    keywords = browser.find_element_by_name('keywords').send_keys('keywords')
    short_description = browser.find_element_by_name('short_description[en]').send_keys('short_description')
    description = browser.find_element_by_name('description[en]').send_keys('description')
    head_title = browser.find_element_by_name('head_title[en]').send_keys('head_title')
    meta_description = browser.find_element_by_name('meta_description[en]').send_keys('meta_description')

def swich_to_prices(browser):
    tabs = browser.find_element_by_class_name('index')
    tab = tabs.find_elements_by_tag_name('li')
    price = tab[3]
    price.click()
    time.sleep(2)

def full_fields_price(browser):
    purchase_price = browser.find_element_by_name('purchase_price')
    purchase_price.clear()
    purchase_price.send_keys('5')
    purchase_price_select = browser.find_element_by_xpath("//select[@name='purchase_price_currency_code']/option[@value='USD']").click()
    price_usd = browser.find_element_by_name('prices[USD]').send_keys('5')
    price_eur = browser.find_element_by_name('prices[EUR]').send_keys('5')

def save_product(browser):
    button_save = browser.find_element_by_name('save').click()
    time.sleep(2)

def how_manu_products(browser):
    countries_table = browser.find_element_by_class_name('dataTable')
    return len(countries_table.find_elements_by_tag_name('tr')[2:-1])


