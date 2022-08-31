import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


LINK = 'http://localhost/litecart/en/'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    # для устранения перестройки DOM, отключила JS
    chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(2)
    #browser = webdriver.Firefox()

    yield browser

    browser.quit()


def test_basket(browser):
    browser.get(LINK)

    for commodity_index in range(1,4):
        open_first_product(browser)
        add_product_to_basket(browser)
        check_counter_increase(browser, str(commodity_index))
        go_back_to_the_main_page(browser)

    go_to_basket(browser)
    products_amount = count_products(browser)

    for index in range(1, products_amount+1):
        remove_product(browser, products_amount + 1 - index) # передаем количество оставшихся элементов для обработки карусели

        if has_summary_table(browser):
            new_products_amount = count_products(browser)
        else:
            new_products_amount = products_amount - index

        if products_amount - index != new_products_amount:
            pytest.fail()
        


def open_first_product(browser):
    general_menu = browser.find_element_by_id('box-most-popular')
    products = general_menu.find_elements_by_class_name('link')
    duck = products[0]
    duck.click()


def add_product_to_basket(browser):
    if has_selector(browser):
        select_value(browser)
    add = browser.find_element_by_name('add_cart_product').click()

def has_selector(browser):
    try:
        browser.find_element_by_class_name('options')
        return True
    except NoSuchElementException:
        return False


def select_value(browser):
    browser.find_element_by_xpath("//select[@name='options[Size]']/option[@value='Small']").click()


def check_counter_increase(browser, param):
        wait = WebDriverWait(browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart > a.content > span.quantity') , param))


def get_crumbs(browser):
    crumbs = browser.find_elements_by_class_name('list-horizontal')[1]
    home = crumbs.find_elements_by_tag_name('li')[0]

    return home.find_element_by_tag_name('a')


def go_back_to_the_main_page(browser):
    get_crumbs(browser).click()


def get_link_cart(browser):
    cart = browser.find_element_by_id('cart')

    return cart.find_elements_by_tag_name('a')[2]


def go_to_basket(browser):
    get_link_cart(browser).click()


def remove_product(browser, elements_amount):
    remove_button = browser.find_element_by_name('remove_cart_item')
    for element in range(0, elements_amount):

        try:
            remove_button.click()
            break

        except ElementNotInteractableException:
            # если в момент нажатия сработала карусель - кликаем еще раз
            time.sleep(1)
            continue


def count_products(browser):
    summary = browser.find_element_by_id('box-checkout-summary')
    table = summary.find_element_by_tag_name('table')
    table_rows = table.find_elements_by_tag_name('tr')

    products_amount = parse_summary_table(table_rows)

    return products_amount


def parse_summary_table(table_rows):
    counter = 0

    for row in table_rows[1:]:  # исключаем хэдер таблицы
        if row_contets_product(row):
            counter += 1

    return counter


def row_contets_product(row):
    row_attributes = row.find_elements_by_tag_name('td')

    return validate_row_attributes(row_attributes)


def validate_row_attributes(row_attributes):
    try:
        item_ceil = row_attributes[1]
        return item_ceil.get_attribute('class') == 'item'
    except IndexError:
        return False


def get_line_table(browser):
    table = browser.find_element_by_class_name('rounded-corners')

    return len(table.find_elements_by_tag_name('tr'))


def table_increase(browser):
    table = get_line_table(browser)
    line_table = table - 5
    wait = WebDriverWait(browser, 5)
    wait.until(EC.staleness_of(line_table))


def has_summary_table(browser):
    try:
        browser.find_element_by_id('box-checkout-summary')
    except NoSuchElementException:
        return False

    return True


