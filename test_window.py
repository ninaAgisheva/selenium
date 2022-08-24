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
    browser.implicitly_wait(2)

    authorize(browser)

    yield browser  # тут урпавление передается тесту

    browser.quit()


def authorize(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button_login = browser.find_element_by_name('login').click()


def test_window(browser):
    add_new_country(browser)
    check_links(browser)


def add_new_country(browser):
    browser.find_element_by_class_name('button').click()


def check_links(browser):
    for field in get_table_rows(browser):
        data = get_row_data(field)
        if has_link(data):
            link = get_link(data)
            verify_link(browser, link)


def get_table_rows(browser):
    table = browser.find_elements_by_tag_name('tbody')[1]
    return table.find_elements_by_tag_name('tr')


def get_row_data(field):
    return field.find_element_by_tag_name('td')


def has_link(data):
    try:
        data.find_element_by_tag_name('a')
    except NoSuchElementException:
        return False
    return True


def get_link(data):
    link_element = data.find_elements_by_tag_name('a')

    #обработка кейса с вопросом-ссылкой
    if len(link_element) == 1:
        return link_element[0].get_attribute('href')

    return link_element[1].get_attribute('href')


def verify_link(browser, link):
    browser.implicitly_wait(2)
    tab_one = browser.window_handles[0]
    browser.execute_script("window.open('');")
    tab_two = browser.window_handles[1]
    browser.switch_to.window(tab_two)
    browser.get(link)
    time.sleep(2)
    browser.close()
    browser.switch_to.window(tab_one)


