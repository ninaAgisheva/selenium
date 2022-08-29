import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select


LINK = 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)

    authorize(browser)

    yield browser

    browser.quit()


def authorize(browser):
    browser.get(LINK)
    login = browser.find_element_by_name('username').send_keys('admin')
    password = browser.find_element_by_name('password').send_keys('admin')
    button_login = browser.find_element_by_name('login').click()


def test_sort_countries(browser):
    countries_with_zone_list = get_countries_with_zones_lists(browser)

    check_zones_sorted_properly(browser, countries_with_zone_list)


def check_zones_sorted_properly(browser, countries_with_zone_list):
    for country_link in countries_with_zone_list:
        zone_list = get_list_of_zones(browser, country_link)

        check_that_list_is_sorted(zone_list)


def get_list_of_zones(browser, country_link):
    browser.get(country_link)
    table_of_zones = browser.find_element_by_id('table-zones')
    table_rows = table_of_zones.find_elements_by_tag_name('tr')[1:-1]

    list_of_zones = []

    for row in table_rows:
        zone_list = row.find_elements_by_tag_name('td')[2]
        zone_select_element = zone_list.find_element_by_tag_name('select')
        zone_selector = Select(zone_select_element)
        selected_option = zone_selector.first_selected_option.text
        list_of_zones.append(selected_option)
    return list_of_zones


def check_that_list_is_sorted(some_list):
    some_list_copy = some_list.copy()

    assert sorted(some_list_copy) == some_list


def get_countries_with_zones_lists(browser):
    countries_table = browser.find_element_by_class_name('dataTable')
    rows = countries_table.find_elements_by_tag_name('tr')[1:-1]

    countries_with_zone = []

    for row in rows:
        countries_with_zone.append(get_country_name_link(row))

    return countries_with_zone


def get_country_name_link(row):
    return get_country_name(row).get_attribute('href')


def get_country_name(row):
    country_name_ceil = row.find_elements_by_tag_name('td')[4]

    return country_name_ceil.find_element_by_tag_name('a')
