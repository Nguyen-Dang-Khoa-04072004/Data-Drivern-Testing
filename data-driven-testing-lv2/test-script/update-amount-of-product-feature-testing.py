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
        self.driver.get(self.data['homeUrl'])
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
    def find_element(self, how : str, value : str):
        try: 
            if how == "ID":
                elenment = self.driver.find_element(by=By.ID, value=value)
            elif how == "CLASS":
               elenment = self.driver.find_element(by=By.CLASS_NAME, value=value) 
            elif how == "XPATH":
               elenment = self.driver.find_element(by=By.XPATH, value=value) 
            elif how == "CSS":
                elenment = self.driver.find_element(by=By.CSS_SELECTOR, value=value)
            elif how == "LINK":
                 elenment = self.driver.find_element(by=By.LINK_TEXT, value=value) 
        except NoSuchElementException as e: 
            return None ,False
        return elenment ,True
    def execute_add_product_to_cart(self):
        self.driver.get(f"{self.data['searchUrl']}&search={self.data['productName'].replace(" ","+")}")
        self.driver.implicitly_wait(50)
        productItem, isProductItemPresent = self.find_element(how=self.data['productItem']['by'],value=self.data['productItem']['value'])
        self.assertTrue(isProductItemPresent)
        productItem.click()
        viewCartButton, isViewCartButtonPresent  = self.find_element(how=self.data['viewCartButton']['by'],value=self.data['viewCartButton']['value'])
        self.assertTrue(isViewCartButtonPresent)
        viewCartButton.click()
        self.driver.implicitly_wait(50)
    def modify_quantity_and_click_update(self, value : int):
        self.driver.get(self.data['cartUrl'])
        self.driver.implicitly_wait(30)
        quantityInput, isQuantityInputPresent = self.find_element(how=self.data['quantityInput']['by'],value=self.data['quantityInput']['value'])
        self.assertTrue(isQuantityInputPresent)
        quantityInput.click()
        quantityInput.clear()
        quantityInput.send_keys(value)
        updateButton, isUpdateButtonPresent = self.find_element(how=self.data['updateButton']['by'],value=self.data['updateButton']['value'])
        self.assertTrue(isUpdateButtonPresent)
        updateButton.click()
        time.sleep(2)
    def check_update_quantity_successfully(self, value : str):
        alertDiv, isAlertDivPresent = self.find_element(how=self.data['alertDiv']['by'],value=self.data['alertDiv']['value'])
        quantityInput, isQuantityInputPresent = self.find_element(how=self.data['quantityInput']['by'],value=self.data['quantityInput']['value'])
        self.assertTrue(isQuantityInputPresent) 
        self.assertTrue(isAlertDivPresent)
        self.assertEqual(quantityInput.get_attribute("value"),str(value))
        self.assertEqual(re.sub(r'[^A-Za-z0-9]','',alertDiv.text.strip()),"SuccessYouhavemodifiedyourshoppingcart")
    def check_empty_cart(self):
        pageTitle , isPageTitlePresent = self.find_element(how=self.data['pageTitle']['by'],value=self.data['pageTitle']['value'])
        content, isContentPresent = self.find_element(how=self.data['content']['by'],value=self.data['content']['value'])
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
