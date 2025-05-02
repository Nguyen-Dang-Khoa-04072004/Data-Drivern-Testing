# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import unittest, time, re
import json

class LoginFeatureSuite(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.data = self.readTestData("../data/login-data.json")
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get(self.data['loginUrl'])
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
        except NoSuchElementException as e: 
            return None ,False
        return elenment ,True
    def find_element_and_enter_value_and_click_login_button(self, emailValue: str, passwordValue : str):
        emailInput, isEmailInputPresent = self.find_element(how=self.data['emailInput']['by'],value=self.data['emailInput']['value'])
        self.assertTrue(isEmailInputPresent)
        self.enter_value(element=emailInput, value=emailValue)
        passwordInput, isPasswordInputPresent = self.find_element(how=self.data['passwordInput']['by'],value=self.data['passwordInput']['value'])
        self.assertTrue(isPasswordInputPresent)
        self.enter_value(passwordInput,value=passwordValue)
        loginButton, isLoginButtonPresent = self.find_element(how=self.data['loginButton']['by'],value=self.data['loginButton']['value'])
        self.assertTrue(isLoginButtonPresent)
        loginButton.click()
    def check_login_failed(self):
        alertDiv , isAlertDivPresent = self.find_element(how=self.data['alertDiv']['by'],value=self.data['alertDiv']['value'])
        self.assertTrue(isAlertDivPresent)
        self.assertEqual("Warning: No match for E-Mail Address and/or Password.",alertDiv.text)
    def check_login_successfully(self):
        login_successful_url = self.data['loginSuccessUrl']
        login_success_title = "My Account"
        self.driver.get(login_successful_url)
        self.assertEqual(self.driver.current_url.strip(), login_successful_url)
        self.assertEqual(self.driver.title.strip(),login_success_title)
        
    def test_login_with_invalid_emai_and_invalid_password(self):
        self.find_element_and_enter_value_and_click_login_button(
            emailValue=self.data['invalidEmailAndInvalidPassword']['email'],
            passwordValue=self.data['invalidEmailAndInvalidPassword']['password']
        )
        self.driver.implicitly_wait(50)
        self.check_login_failed()
        
    def test_login_with_invalid_email_and_valid_password(self):
        self.find_element_and_enter_value_and_click_login_button(
            emailValue=self.data['invalidEmailAndValidPassword']['email'],
            passwordValue=self.data['invalidEmailAndValidPassword']['password']
        )
        self.driver.implicitly_wait(50)
        self.check_login_failed() 

    def test_login_with_valid_email_and_invalid_password(self):
        self.find_element_and_enter_value_and_click_login_button(
            emailValue=self.data['validEmailAndInvalidPassword']['email'],
            passwordValue=self.data['validEmailAndInvalidPassword']['password']
        )
        self.driver.implicitly_wait(50)
        self.check_login_failed() 
        
    def test_login_with_valid_emai_and_valid_password(self):
        self.find_element_and_enter_value_and_click_login_button(
            emailValue=self.data['validEmailAndValidPassword']['email'],
            passwordValue=self.data['validEmailAndValidPassword']['password']
        )
        self.driver.implicitly_wait(50)
        self.check_login_successfully() 
    def tearDown(self):
        self.driver.get(self.data['logoutUrl'])
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
