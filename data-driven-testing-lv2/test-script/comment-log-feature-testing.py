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
        self.data = self.readTestData("../data/comment-blog-data.json")
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.get(self.data['blogUrl'])
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
    def find_element_and_enter_value_and_click_comment_button(self,nameValue: str, emailValue: str, commentValue : str):
        nameInput, isNameInputPresent = self.find_element(how=self.data['nameInput']['by'],value=self.data['nameInput']['value'])
        self.assertTrue(isNameInputPresent)
        self.enter_value(element=nameInput, value=nameValue)
        
        emailInput, isEmailInputPresent = self.find_element(how=self.data['emailInput']['by'],value=self.data['emailInput']['value'])
        self.assertTrue(isEmailInputPresent)
        self.enter_value(element=emailInput, value=emailValue)
        
        commentInput, isCommentInputPresent = self.find_element(how=self.data['commentInput']['by'],value=self.data['commentInput']['value'])
        self.assertTrue(isCommentInputPresent)
        self.enter_value(commentInput,value=commentValue)
        
        commentButton, isCommentButtonPresent = self.find_element(how=self.data['commentButton']['by'],value=self.data['commentButton']['value'])
        self.assertTrue(isCommentButtonPresent)
        commentButton.click()
        
        self.driver.implicitly_wait(50)
    def check_comment_blog_successfully(self):
        alertDiv, isAlertDivPresent = self.find_element(how=self.data['alertDiv']['by'],value=self.data['alertDiv']['value'])
        self.assertTrue(isAlertDivPresent)
        self.assertEqual(re.sub(r'[^A-Za-z0-9]','',alertDiv.text.strip()),"ThankyouforyourcommentIthasbeensubmittedtothewebmasterforapproval")
    def check_invalid_fields(self,name=True, email=True, comment=True):
        if not name:
            message, isMessagePresent = self.find_element(how=self.data['warning1']['by'],value=self.data['warning1']['value'])
            self.assertTrue(isMessagePresent)
            self.assertEqual(re.sub(r'[^A-Za-z0-9]','',message.text.strip()), "WarningCommentNamemustbebetween3and25characters")
        if not email:
            message, isMessagePresent = self.find_element(how=self.data['warning2']['by'],value=self.data['warning2']['value'])
            self.assertTrue(isMessagePresent)
            self.assertEqual(re.sub(r'[^A-Za-z0-9]','',message.text.strip()), "WarningInvalidemailid")
        if not comment:
            message, isMessagePresent = self.find_element(how=self.data['warning3']['by'],value=self.data['warning3']['value'])
            self.assertTrue(isMessagePresent)
            self.assertEqual(re.sub(r'[^A-Za-z0-9]','',message.text.strip()), "WarningCommentTextmustbebetween25and1000characters") 
    def test_rule_01(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['validName'],
            emailValue=self.data['validEmail'],
            commentValue=self.data['validComment']
        )
        time.sleep(2)
        self.check_comment_blog_successfully()
    def test_rule_02(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['validName'],
            emailValue=self.data['inValidEmail'],
            commentValue=self.data['validComment']
        )
        time.sleep(2)
        self.check_invalid_fields(email=False)
    def test_rule_03(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['validName'],
            emailValue=self.data['validEmail'],
            commentValue=self.data['inValidComment']
        )
        time.sleep(2)
        self.check_invalid_fields(comment=False)
    def test_rule_04(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['validName'],
            emailValue=self.data['inValidEmail'],
            commentValue=self.data['inValidComment']
        )
        time.sleep(2)
        self.check_invalid_fields(comment=False, email=False)
    def test_rule_05(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['inValidName'],
            emailValue=self.data['validEmail'],
            commentValue=self.data['validComment']
        )
        time.sleep(2)
        self.check_invalid_fields(name=False)
    def test_rule_06(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['inValidName'],
            emailValue=self.data['inValidEmail'],
            commentValue=self.data['validComment']
        )
        time.sleep(2)
        self.check_invalid_fields(name=False, email=False)
    def test_rule_07(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['inValidName'],
            emailValue=self.data['validEmail'],
            commentValue=self.data['inValidComment']
        )
        time.sleep(2)
        self.check_invalid_fields(name=False,comment=False)
    def test_rule_08(self):
        self.find_element_and_enter_value_and_click_comment_button(
            nameValue=self.data['inValidName'],
            emailValue=self.data['inValidEmail'],
            commentValue=self.data['inValidComment']
        )
        time.sleep(2)
        self.check_invalid_fields(name=False,email=False,comment=False)
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
