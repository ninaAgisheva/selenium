import pytest


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LINK = 'https://github.com/ninaAgisheva/selenium'


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