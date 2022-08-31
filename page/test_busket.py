import pytest

from .locators import *
from .base_page import BasePage
from .form_product_page import ProductPage


URL = 'http://localhost/litecart/en/'


def test_basket(browser):
    page = ProductPage(browser, URL)
    page.open_page()

    for commodity_index in range(1,4):
        page.open_first_product()
        page.add_product_to_basket()
        page.check_counter_increase(str(commodity_index))
        page.go_back_to_the_main_page()

    page.go_to_basket()
    products_amount = page.count_products()

    for index in range(1, products_amount+1):
        page.remove_product(products_amount + 1 - index) # передаем количество оставшихся элементов для обработки карусели

        if page.has_summary_table():
            new_products_amount = page.count_products()
        else:
            new_products_amount = products_amount - index

        if products_amount - index != new_products_amount:
            pytest.fail()
