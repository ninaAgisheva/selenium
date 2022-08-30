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

    main_title = get_name_on_main_page(browser)
    main_price = get_price(browser, get_product, 's')
    main_sale_price = get_price(browser, get_product, 'strong')
    main_color_price = get_color(browser, get_product, 's')
    parse_color_gray(main_color_price)
    main_color_sale_price = get_color(browser, get_product,'strong')
    parse_color_red(main_color_sale_price)
    main_size_price = get_size(browser, get_product, 's')
    main_size_sale_price = get_size(browser, get_product, 'strong')
    tag_main_price = get_tag(browser, get_product, 'regular-price')
    tag_main_sale_price = get_tag(browser, get_product, 'campaign-price')

    assert main_size_price < main_size_sale_price
    assert main_size_price != main_size_sale_price
    assert tag_main_price == 's'
    assert tag_main_sale_price == 'strong'


    go_to_cart_product(browser)

    product_title = get_name_on_product_page(browser)
    product_price = get_price(browser, get_cart_product, 's')
    product_sale_price = get_price(browser, get_cart_product, 'strong')
    product_color_price = get_color(browser, get_cart_product,'s')
    parse_color_gray(product_color_price)
    product_color_sale_price = get_color(browser, get_cart_product, 'strong')
    parse_color_red(product_color_sale_price)
    product_size_price = get_size(browser, get_cart_product, 's')
    product_size_sale_price = get_size(browser, get_cart_product, 'strong')
    tag_product_price = get_tag(browser, get_cart_product, 'regular-price')
    tag_product_sale_price = get_tag(browser, get_cart_product, 'campaign-price')

    assert product_size_price < product_size_sale_price 
    assert product_size_price != product_size_sale_price 
    assert tag_product_price == 's' 
    assert tag_product_sale_price == 'strong' 
    assert main_title == product_title 
    assert main_price == product_price 
    assert main_sale_price == product_sale_price


def get_product(browser):
    campaigns = browser.find_element_by_id('box-campaigns')
    product = campaigns.find_element_by_tag_name('li')

    return product.find_element_by_tag_name('a')


def get_name_on_main_page(browser):
    product = get_product(browser)

    return product.get_attribute('title')


def get_name_on_product_page(browser):
    product = get_cart_product(browser)

    return product.find_element_by_class_name('title').text


def get_price(browser, get_product_function, tag_name):
    product = get_product_function(browser)
    price = product.find_element_by_class_name('price-wrapper')

    return price.find_element_by_tag_name(tag_name).text


def get_color(browser, get_product_function, tag_name):
    product = get_product_function(browser)
    price = product.find_element_by_class_name('price-wrapper')

    return price.find_element_by_tag_name(tag_name).value_of_css_property("color")


def parse_color_gray(color_string):
    color = color_string.split('(')[1]
    color_RGB = color.split(')')[0]
    R, G, B, ignore = color_RGB.split(', ')

    assert R == G == B

def parse_color_red(color_string):
    color = color_string.split('(')[1]
    color_RGB = color.split(')')[0]
    R, G, B, ignore = color_RGB.split(', ')

    assert G == B


def get_size(browser, get_product_function, tag_name):
    product = get_product_function(browser)
    price = product.find_element_by_class_name('price-wrapper')
    size_text = price.find_element_by_tag_name(tag_name).value_of_css_property("font-size")
    size = float(size_text.replace('px', ''))

    return size


def get_tag(browser, get_product_function, class_name):
    product = get_product_function(browser)

    return product.find_element_by_class_name(class_name).tag_name


def go_to_cart_product(browser):
    get_product(browser).click()


def get_cart_product(browser):

    return browser.find_element_by_id('box-product')

