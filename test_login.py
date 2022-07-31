import pytest


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LINK = 'http://localhost/litecart/admin/login.php'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')  
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    yield browser  # тут урпавление передается тесту

    browser.quit()


def test_basket(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button = browser.find_element_by_name('login').click
