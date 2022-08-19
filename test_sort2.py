import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


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
    press_button_countries(browser)
    all_countries_list, countries_with_zone_list = get_all_countries_and_countries_with_zones_lists(browser)

    check_all_countries_sorted_properly(all_countries_list)
    check_zones_sorted_properly(browser, countries_with_zone_list)


def check_all_countries_sorted_properly(all_countries_list):
    check_that_list_is_sorted(all_countries_list)


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
        name = row.find_elements_by_tag_name('td')[2].text
        list_of_zones.append(name)

    return list_of_zones


def check_that_list_is_sorted(some_list):
    some_list_copy = some_list.copy()

    assert sorted(some_list_copy) == some_list


def get_all_countries_and_countries_with_zones_lists(browser):
    countries_table = browser.find_element_by_class_name('dataTable')
    rows = countries_table.find_elements_by_tag_name('tr')[1:-1]

    countries_list = []
    countries_with_zone = []

    for row in rows:
        countries_list.append(get_country_name_text(row))

        if has_zone(row):
            countries_with_zone.append(get_country_name_link(row))

    return countries_list, countries_with_zone


def has_zone(row):
    return int(row.find_elements_by_tag_name('td')[5].text) > 0


def get_country_name_text(row):
    return get_country_name(row).text


def get_country_name_link(row):
    return get_country_name(row).get_attribute('href')


def get_country_name(row):
    country_name_ceil = row.find_elements_by_tag_name('td')[4]

    return country_name_ceil.find_element_by_tag_name('a')
