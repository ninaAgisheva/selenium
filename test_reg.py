import pytest
import time
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

LINK = 'http://localhost/litecart/en/create_account'
pwd = 'password'

@pytest.fixture
def browser():
    #Schrome_options = Options()
    #chrome_options.add_argument('--window-size=1920,1080')  
    #browser = webdriver.Chrome(options=chrome_options)
    #browser.implicitly_wait(10)
    browser = webdriver.Firefox()

    yield browser  

    browser.quit()

def test_create_account(browser):
    browser.get(LINK)
    full_fields(browser)
    log_out(browser)
    authorize(browser)

def authorize(browser):
    email = browser.find_element_by_name('email').send_keys(generate_email())
    password = browser.find_element_by_name('password').send_keys(pwd)
    button_login = browser.find_element_by_name('login').click()

def log_out(browser):
    account = browser.find_element_by_id('box-account')
    row = account.find_elements_by_tag_name('li')
    log_out = row[3]
    link = log_out.find_element_by_tag_name('a')
    link.click()

def full_fields(browser):
    tax_id = browser.find_element_by_name('tax_id').send_keys('tax_id')
    company = browser.find_element_by_name('company').send_keys('company')
    first_name = browser.find_element_by_name('firstname').send_keys('firstname')
    last_name = browser.find_element_by_name('lastname').send_keys('lastname')
    address1 = browser.find_element_by_name('address1').send_keys('address1')
    address2 = browser.find_element_by_name('address2').send_keys('address2')
    postcode = browser.find_element_by_name('postcode').send_keys('12345')
    city = browser.find_element_by_name('city').send_keys('city')
    country = list_country(browser)
    email = browser.find_element_by_name('email').send_keys(generate_email())
    phone = browser.find_element_by_name('phone').send_keys('+70000456754')
    desired_password = browser.find_element_by_name('password').send_keys(pwd)
    confirm_password = browser.find_element_by_name('confirmed_password').send_keys(pwd)
    create_account = browser.find_element_by_name('create_account').click()

def list_country(browser):
    country = browser.find_element_by_class_name('select2-selection__rendered').click()
    pole = browser.find_element_by_class_name('select2-search__field')
    pole.send_keys('United States')
    pole.send_keys(Keys.ENTER)

def generate_email():
        return ''.join(random.choice(string.ascii_letters) for _ in range(7)) + "@gmail.com"


