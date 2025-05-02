# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import unittest, time, re
import json

class EditCartFeatureSuite(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.data = self.readTestData("../data/edit-cart-data.json")
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get(self.data['homeUrl'])
        self.driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", "display_grid", "list")
        self.verificationErrors = []
    def readTestData(self, filepath : str):
        with open(file=filepath, mode='r') as file:
            return json.load(file)
    def enter_value(self, element : WebElement, value: str):
        element.click()
        element.clear()
        element.send_keys(value)
    def find_all_element(self, how : str, value : str):
        try: 
            if how == "ID":
                elenment = self.driver.find_elements(by=By.ID, value=value)
            elif how == "CLASS":
                elenment = self.driver.find_elements(by=By.CLASS_NAME, value=value) 
            elif how == "XPATH":
                elenment = self.driver.find_elements(by=By.XPATH, value=value) 
            elif how == "CSS":
                elenment = self.driver.find_elements(by=By.CSS_SELECTOR, value=value)
            elif how == "LINK":
                elenment = self.driver.find_elements(by=By.LINK_TEXT, value=value) 
        except NoSuchElementException as e: 
            return None ,False
        return elenment ,True
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
    def execute_add_product_to_cart(self, productName: str, productId: int):
        self.driver.get(f"{self.data['searchUrl']}&search={productName.replace(" ","+")}")
        self.driver.implicitly_wait(50)
        productItem = self.driver.find_element(by=By.XPATH,value=f'''//button[@onclick="cart.add('{productId}');"]''')
        productItem.click()
        self.driver.implicitly_wait(50)
        viewCartButton, isViewCartButtonPresent  = self.find_element(how=self.data['viewCartButton']['by'],value=self.data['viewCartButton']['value'])
        self.assertTrue(isViewCartButtonPresent)
        viewCartButton.click()
        self.driver.implicitly_wait(50)
    def click_checkout_button(self):
        self.driver.implicitly_wait(30)
        checkoutButton, isCheckoutButtonPresent = self.find_element(how=self.data['checkoutButton']['by'],value=self.data['checkoutButton']['value'])
        self.assertTrue(isCheckoutButtonPresent)
        checkoutButton.click()
        self.driver.implicitly_wait(50)
    def click_continue_shopping_button(self):
        self.driver.implicitly_wait(30)
        continueShoppingButton, isContinueShoppingButtonPresent = self.find_element(how=self.data['continueShoppingButton']['by'],value=self.data['continueShoppingButton']['value'])
        self.assertTrue(isContinueShoppingButtonPresent)
        continueShoppingButton.click()
        self.driver.implicitly_wait(50)
    def click_remove_item_button(self, isAll = True):
        if isAll:
            removeButtons, isRemoveButtonsPresent = self.find_all_element(how=self.data['removeButton']['by'],value=self.data['removeButton']['value'])
            self.assertTrue(isRemoveButtonsPresent)
            for removeButton in removeButtons:
                removeButton.click()
                self.driver.implicitly_wait(30)
        else:
            removeButton, isRemoveButtonPresent = self.find_element(how=self.data['removeButton']['by'],value=self.data['removeButton']['value'])
            self.assertTrue(isRemoveButtonPresent)
            removeButton.click()
            self.driver.implicitly_wait(30)
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
    def check_show_warning(self):
        alertDiv, isAlertDivPresent = self.find_element(how=self.data['alertDivDanger']['by'],value=self.data['alertDivDanger']['value'])
        self.assertTrue(isAlertDivPresent)
        self.assertEqual(re.sub(r'[^A-Za-z0-9]','',alertDiv.text.strip()),"Productsmarkedwitharenotavailableinthedesiredquantityornotinstock")
    def check_on_home_page(self):
        self.assertIn("Your Store",self.driver.title)
        self.assertIn(self.data['homeUrl'],self.driver.current_url)
    def check_on_checkout_page(self):
        self.assertIn("Checkout",self.driver.title)
        self.assertIn(self.data['checkoutUrl'],self.driver.current_url)
    def check_empty_cart(self):
        pageTitle , isPageTitlePresent = self.find_element(how=self.data['pageTitle']['by'],value=self.data['pageTitle']['value'])
        content, isContentPresent = self.find_element(how=self.data['content']['by'],value=self.data['content']['value'])
        self.assertTrue(isPageTitlePresent)
        self.assertTrue(isContentPresent)
        self.assertEqual(content.text.strip(),"Your shopping cart is empty!")
        self.assertEqual(pageTitle.text.strip(),"Shopping Cart")
    def check_is_product_not_in_cart(self, productName : str):
        products, _ = self.find_all_element(how=self.data['products']['by'],value=self.data['products']['value'])
        self.assertNotIn(productName,[product.text for product in products])
    def test_checkout_with_out_of_stock_product(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.click_checkout_button()
        self.check_show_warning()
    def test_checkout_with_in_stock_product(self):
        self.execute_add_product_to_cart(productName=self.data['inStockProductName'],productId=self.data['inStockProductId'])
        self.click_checkout_button() 
        self.check_on_checkout_page()
    def test_continue_shopping(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.click_continue_shopping_button()
        self.check_on_home_page()
    def test_remove_one_item(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.execute_add_product_to_cart(productName=self.data['inStockProductName'],productId=self.data['inStockProductId']) 
        self.click_remove_item_button(isAll=False)
        time.sleep(1)
        self.check_is_product_not_in_cart(productName=self.data['outOfStockProductName'])
    def test_remove_all_items(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.execute_add_product_to_cart(productName=self.data['inStockProductName'],productId=self.data['inStockProductId']) 
        self.click_remove_item_button(isAll=True)
        time.sleep(1) 
        self.check_empty_cart()
    def test_modify_quantity_of_product_with_valid_quantity(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.modify_quantity_and_click_update(self.data['validQuantity'])
        self.check_update_quantity_successfully(self.data['validQuantity'])
    def test_modify_quantity_of_product_with_invalid_quantity(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.modify_quantity_and_click_update(self.data['inValidQuantity'])
        time.sleep(1)
        self.check_empty_cart()
    def test_modify_quantity_of_product_with_invalid_quantity_when_have_mutiple_product(self):
        self.execute_add_product_to_cart(productName=self.data['inStockProductName'],productId=self.data['inStockProductId'])  
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.modify_quantity_and_click_update(self.data['inValidQuantity'])
        time.sleep(1)
        self.check_is_product_not_in_cart(productName=self.data['outOfStockProductName'])
    def test_modify_quantity_of_product_with_valid_quantity(self):
        self.execute_add_product_to_cart(productName=self.data['outOfStockProductName'],productId=self.data['outOfStockProductId'])
        self.modify_quantity_and_click_update(self.data['outRangeQuantity'])
        self.check_update_quantity_successfully(str(2147483647)) 
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
