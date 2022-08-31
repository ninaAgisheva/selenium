import os
import pytest
import random
import string
import time

from .base_page import BasePage
from .locators import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class ProductPage(BasePage):


    def open_first_product(self):
        general_menu = self.browser.find_element(*MainPageLocators.GENERAL_MENU)
        products = general_menu.find_elements(*MainPageLocators.PRODUKTS)
        duck = products[0]
        duck.click()


    def add_product_to_basket(self):
        if self.has_selector():
            self.select_value()
        kek = self.browser.find_element(*MainPageLocators.ADD)
        kek.click()


    def has_selector(self):
        try:
            self.browser.find_element(*ProductPageLocators.SIZE)
            return True
        except NoSuchElementException:
            return False


    def select_value(self):
        self.browser.find_element(*ProductPageLocators.SIZE_SELECT).click()


    def check_counter_increase(self, param):
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart > a.content > span.quantity') , param))


    def get_crumbs(self):
        crumbs = self.browser.find_element(*ProductPageLocators.CRAMBS)
        home = crumbs.find_elements(*ProductPageLocators.HOME)[0]

        return home.find_element(*ProductPageLocators.HOME_CRAMBS)


    def go_back_to_the_main_page(self):
        self.get_crumbs().click()


    def get_link_cart(self):
        cart = self.browser.find_element(*MainPageLocators.CART)

        return cart.find_elements(*MainPageLocators.LINK_CART)[2]


    def go_to_basket(self):
        self.get_link_cart().click()


    def remove_product(self, elements_amount):
        remove_button = self.browser.find_element(*ProductPageLocators.BUTTON_REMOVE)
        for element in range(0, elements_amount):

            try:
                remove_button.click()
                break

            except ElementNotInteractableException:
                # если в момент нажатия сработала карусель - кликаем еще раз
                time.sleep(1)
                continue


    def count_products(self):
        summary = self.browser.find_element(*ProductPageLocators.SUMMARY)
        table = summary.find_element(*ProductPageLocators.TABLE)
        table_rows = table.find_elements(*ProductPageLocators.TABLE_ROWS)

        products_amount = self.parse_summary_table(table_rows)

        return products_amount


    def parse_summary_table(self, table_rows):
        counter = 0

        for row in table_rows[1:]:  # исключаем хэдер таблицы
            if self.row_contets_product(row):
                counter += 1

        return counter


    def row_contets_product(self, row):
        row_attributes = row.find_elements(*ProductPageLocators.ROW_ATTRIBUTES)

        return self.validate_row_attributes(row_attributes)


    def validate_row_attributes(self, row_attributes):
        try:
            item_ceil = row_attributes[1]
            return item_ceil.get_attribute('class') == 'item'
        except IndexError:
            return False


    def get_line_table(self):
        table = self.browser.find_element(*ProductPageLocators.TABLE)

        return len(table.find_elements(*ProductPageLocators.TABLE_ROWS))


    def table_increase(self):
        table = get_line_table(self.browser)
        line_table = table - 5
        wait = WebDriverWait(self.browser, 5)
        wait.until(EC.staleness_of(line_table))


    def has_summary_table(self):
        try:
            self.browser.find_element(*ProductPageLocators.SUMMARY)
        except NoSuchElementException:
            return False

        return True
