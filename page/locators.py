from selenium.webdriver.common.by import By

class MainPageLocators():
    """
    локаторы с главной страницы
    """
    GENERAL_MENU = (By.ID, 'box-most-popular')
    PRODUKTS = (By.CLASS_NAME, 'link')
    ADD = (By.NAME, 'add_cart_product')
    CART = (By.ID, 'cart')
    LINK_CART = (By.TAG_NAME, 'a')


class ProductPageLocators():
    """
    локаторы с cnhfybws njdfhf
    """
    SIZE = (By.CLASS_NAME, 'options')
    SIZE_SELECT = (By.XPATH, "//select[@name='options[Size]']/option[@value='Small']")
    CRAMBS = (By.ID, 'breadcrumbs')
    HOME = (By.TAG_NAME, 'li')
    HOME_CRAMBS = (By.TAG_NAME, 'a')
    BUTTON_REMOVE = (By.NAME, 'remove_cart_item')
    AMOUNT_PRODUCTS = (By.CLASS_NAME, 'shortcuts')
    PRODUCT = (By.TAG_NAME, 'shortcut')
    SUMMARY = (By.ID, 'box-checkout-summary')
    TABLE = (By.TAG_NAME, 'table')
    TABLE_ROWS = (By.TAG_NAME, 'tr')
    ROW_ATTRIBUTES = (By.TAG_NAME, 'td')
