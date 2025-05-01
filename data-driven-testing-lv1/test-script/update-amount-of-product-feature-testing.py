# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import unittest, time, re
import json

class UpdateAmountOfProductFeatureSuite(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.data = self.readTestData("../data/update-amount-of-product-data.json")
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")
        self.driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", "display_grid", "list")
        self.execute_add_product_to_cart()
        self.driver.implicitly_wait(200)
        self.verificationErrors = []
    def readTestData(self, filepath : str):
        with open(file=filepath, mode='r') as file:
            return json.load(file)
    def enter_value(self, element : WebElement, value: str):
        element.click()
        element.clear()
        element.send_keys(value)
    def find_element(self, how : By, value : str):
        try: 
            elenment = self.driver.find_element(by=how, value=value)
        except NoSuchElementException as e: 
            return None ,False
        return elenment ,True
    def execute_add_product_to_cart(self):
        self.driver.get(f"https://ecommerce-playground.lambdatest.io/index.php?route=product%2Fsearch&search={self.data['productName'].replace(" ","+")}")
        self.driver.implicitly_wait(50)
        productItem, isProductItemPresent = self.find_element(how=By.XPATH,value='''//button[@onclick="cart.add('28');"]''')
        self.assertTrue(isProductItemPresent)
        productItem.click()
        self.driver.implicitly_wait(50)
        self.find_element(how=By.LINK_TEXT,value="View Cart")
        self.driver.implicitly_wait(50)
    def modify_quantity_and_click_update(self, value : int):
        self.driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
        self.driver.implicitly_wait(30)
        quantityInput, isQuantityInputPresent = self.find_element(how=By.CLASS_NAME,value="form-control")
        self.assertTrue(isQuantityInputPresent)
        quantityInput.click()
        quantityInput.clear()
        quantityInput.send_keys(value)
        updateButton, isUpdateButtonPresent = self.find_element(how=By.CSS_SELECTOR,value="button.btn.btn-primary")
        self.assertTrue(isUpdateButtonPresent)
        updateButton.click()
        self.driver.implicitly_wait(100)
    def check_update_quantity_successfully(self, value : str):
        alertDiv, isAlertDivPresent = self.find_element(By.CSS_SELECTOR,value="div.alert.alert-success.alert-dismissible")
        quantityInput, isQuantityInputPresent = self.find_element(how=By.CLASS_NAME,value="form-control")
        self.assertTrue(isQuantityInputPresent) 
        self.assertTrue(isAlertDivPresent)
        self.assertEqual(quantityInput.get_attribute("value"),str(value))
        self.assertEqual(re.sub(r'[^A-Za-z0-9]','',alertDiv.text.strip()),"SuccessYouhavemodifiedyourshoppingcart")
    def check_empty_cart(self):
        pageTitle , isPageTitlePresent = self.find_element(how=By.XPATH,value="//div[@id='content']/h1")
        content, isContentPresent = self.find_element(how=By.XPATH,value="//div[@id='content']/p")
        self.assertTrue(isPageTitlePresent)
        self.assertTrue(isContentPresent)
        self.assertEqual(content.text.strip(),"Your shopping cart is empty!")
        self.assertEqual(pageTitle.text.strip(),"Shopping Cart")
    def test_middle_value(self):
        self.modify_quantity_and_click_update(value=self.data['middleValue'])
        self.check_update_quantity_successfully(value=self.data['middleValue'])
    def test_above_lowerBound(self):
        self.modify_quantity_and_click_update(value=self.data['aboveLowerBound'])
        self.check_update_quantity_successfully(value=self.data['aboveLowerBound'])
    def test_below_upperBound(self):
        self.modify_quantity_and_click_update(value=self.data['belowUpperBound'])
        self.check_update_quantity_successfully(value=self.data['belowUpperBound'])
    def test_lowerBound(self):
        self.modify_quantity_and_click_update(value=self.data['lowerBound'])
        self.check_update_quantity_successfully(value=self.data['lowerBound'])
    def test_upperBound(self):
        self.modify_quantity_and_click_update(value=self.data['upperBound'])
        self.check_update_quantity_successfully(value=self.data['upperBound'])
    def test_above_uppperBound(self):
        self.modify_quantity_and_click_update(value=self.data['aboveUpperBound'])
        self.check_update_quantity_successfully(value=self.data['upperBound']) 
    def test_below_lowerBound(self):
        self.modify_quantity_and_click_update(value=self.data['belowLowerBound'])
        self.check_empty_cart() 
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
