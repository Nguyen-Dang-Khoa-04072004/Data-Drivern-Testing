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
        self.driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")
        self.driver.execute_script("localStorage.setItem(arguments[0], arguments[1]);", "display_grid", "list")
        self.verificationErrors = []
    def readTestData(self, filepath : str):
        with open(file=filepath, mode='r') as file:
            return json.load(file)
    def enter_value(self, element : WebElement, value: str):
        element.click()
        element.clear()
        element.send_keys(value)
    def find_all_element(self, how : By, value : str):
        try: 
            elenments = self.driver.find_elements(by=how, value=value)
        except NoSuchElementException as e: 
            return None ,False
        return elenments ,True
    def find_element(self, how : By, value : str):
        try: 
            elenment = self.driver.find_element(by=how, value=value)
        except NoSuchElementException as e: 
            return None ,False
        return elenment ,True
    def execute_add_product_to_cart(self, productName: str, productId: int):
        self.driver.get(f"https://ecommerce-playground.lambdatest.io/index.php?route=product%2Fsearch&search={productName.replace(" ","+")}")
        self.driver.implicitly_wait(50)
        productItem, isProductItemPresent = self.find_element(how=By.XPATH,value=f'''//button[@onclick="cart.add('{productId}');"]''')
        self.assertTrue(isProductItemPresent)
        productItem.click()
        self.driver.implicitly_wait(50)
        viewCartButton, isViewCartButtonPresent  = self.find_element(how=By.LINK_TEXT,value="View Cart")
        self.assertTrue(isViewCartButtonPresent)
        viewCartButton.click()
        self.driver.implicitly_wait(50)
    def click_checkout_button(self):
        self.driver.implicitly_wait(30)
        checkoutButton, isCheckoutButtonPresent = self.find_element(how=By.XPATH,value="//a[contains(text(),'Checkout')]")
        self.assertTrue(isCheckoutButtonPresent)
        checkoutButton.click()
        self.driver.implicitly_wait(50)
    def click_continue_shopping_button(self):
        self.driver.implicitly_wait(30)
        continueShoppingButton, isContinueShoppingButtonPresent = self.find_element(how=By.LINK_TEXT,value="Continue Shopping")
        self.assertTrue(isContinueShoppingButtonPresent)
        continueShoppingButton.click()
        self.driver.implicitly_wait(50)
    def click_remove_item_button(self, isAll = True):
        if isAll:
            removeButtons, isRemoveButtonsPresent = self.find_all_element(how=By.CLASS_NAME,value="btn.btn-danger")
            self.assertTrue(isRemoveButtonsPresent)
            for removeButton in removeButtons:
                removeButton.click()
                self.driver.implicitly_wait(30)
        else:
            removeButton, isRemoveButtonPresent = self.find_element(how=By.CLASS_NAME,value="btn.btn-danger")
            self.assertTrue(isRemoveButtonPresent)
            removeButton.click()
            self.driver.implicitly_wait(30)
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
    def check_show_warning(self):
        alertDiv, isAlertDivPresent = self.find_element(how=By.CLASS_NAME,value="alert.alert-danger.alert-dismissible")
        self.assertTrue(isAlertDivPresent)
        self.assertEqual(re.sub(r'[^A-Za-z0-9]','',alertDiv.text.strip()),"Productsmarkedwitharenotavailableinthedesiredquantityornotinstock")
    def check_on_home_page(self):
        self.assertIn("Your Store",self.driver.title)
        self.assertIn("https://ecommerce-playground.lambdatest.io/index.php?route=common/home",self.driver.current_url)
    def check_on_checkout_page(self):
        self.assertIn("Checkout",self.driver.title)
        self.assertIn("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/checkout",self.driver.current_url)
    def check_empty_cart(self):
        pageTitle , isPageTitlePresent = self.find_element(how=By.XPATH,value="//div[@id='content']/h1")
        content, isContentPresent = self.find_element(how=By.XPATH,value="//div[@id='content']/p")
        self.assertTrue(isPageTitlePresent)
        self.assertTrue(isContentPresent)
        self.assertEqual(content.text.strip(),"Your shopping cart is empty!")
        self.assertEqual(pageTitle.text.strip(),"Shopping Cart")
    def check_is_product_not_in_cart(self, productName : str):
        products, _ = self.find_all_element(how=By.XPATH,value="//div[@id='content']/form/div/table/tbody/tr/td/a")
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
