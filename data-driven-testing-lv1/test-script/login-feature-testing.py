# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class LoginWithInvalidEmaiAndValidPassword(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        self.verificationErrors = []
    
    def test_login_with_invalid_emai_and_valid_password(self):
        self.driver.find_element_by_id("input-email").click()
        self.driver.find_element_by_id("input-email").clear()
        self.driver.find_element_by_id("input-email").send_keys("khoanguyentefabkfst@gmail.com")
        self.driver.find_element_by_id("input-password").click()
        self.driver.find_element_by_id("input-password").clear()
        self.driver.find_element_by_id("input-password").send_keys("123456")
        self.driver.find_element_by_xpath("//input[@value='Login']").click()
        try: self.assertEqual("Warning: No match for E-Mail Address and/or Password.", self.driver.find_element_by_xpath("//div[@id='account-login']/div").text)
        except AssertionError as e: self.verificationErrors.append(str(e))

    def enter_value(self, element : WebElement, value):
            pass
    def find_element(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
