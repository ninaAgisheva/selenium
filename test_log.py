import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select


LINK = 'http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1'


@pytest.fixture
def browser():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities['loggingPrefs'] = { 'browser':'ALL' }

    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options, desired_capabilities=desired_capabilities)
    browser.implicitly_wait(10)

    authorize(browser)

    yield browser

    browser.quit()


def authorize(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button_login = browser.find_element_by_name('login').click()


def test_browser_log(browser):
    check_product(browser)

    logs = browser.get_log('browser')
    assert not logs


def check_product(browser):
    for index in range(5):
        table = browser.find_element_by_class_name('dataTable')
        rows = table.find_elements_by_tag_name('tr')[4:-1]
        href = get_link_product(rows[index])
        browser.get(href)
        exit_from_product(browser)


def get_link_product(row):
    return get_name_product(row).get_attribute('href')


def get_name_product(row):
    name_produkt = row.find_elements_by_tag_name('td')[2]

    return name_produkt.find_element_by_tag_name('a')


def exit_from_product(browser):
    browser.find_element_by_name('cancel').click()
