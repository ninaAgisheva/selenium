import pytest


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    # для устранения перестройки DOM, отключила JS
    chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)
    #browser = webdriver.Firefox()

    yield browser

    browser.quit()
