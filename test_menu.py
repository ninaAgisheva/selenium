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


def get_inner_list(browser, index):
    general_menu = browser.find_element_by_id('box-apps-menu')
    main_menu = general_menu.find_elements(by=By.ID, value='app-')[index]
    inner_elements = main_menu.find_elements_by_tag_name('li')

    if len(inner_elements) == 0:
        return False
    else:
        for inner_index in range(1, len(inner_elements)):
            general_menu = browser.find_element_by_id('box-apps-menu')
            main_menu = general_menu.find_elements(by=By.ID, value='app-')[index]
            inner_elements = main_menu.find_elements_by_tag_name('li')
            inner_elements[inner_index].click()
            validate_header(browser)
            time.sleep(2)


def test_menu(browser):
    for index in range(get_main_menu_length(browser)):
        general_menu = browser.find_element_by_id('box-apps-menu')

        first_range_menu_elements_collection = general_menu.find_elements(by=By.ID, value='app-')
        first_range_menu_elements_collection[index].click()
        validate_header(browser)
        time.sleep(2)
        inner_list = get_inner_list(browser, index)

        if not inner_list:
            continue


def get_main_menu_length(browser):
    general_menu = browser.find_element_by_id('box-apps-menu')
    return len(general_menu.find_elements(by=By.ID, value='app-'))


def validate_header(browser):
    try:
        header = browser.find_element_by_tag_name('h1')
    except NoSuchElementException:
        pytest.fail()
