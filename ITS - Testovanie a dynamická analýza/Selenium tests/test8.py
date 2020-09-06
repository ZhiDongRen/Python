# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
from mySelect import Select

class Test8(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(30)
        self.base_url = "http://mys01.fit.vutbr.cz:8012/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_8(self):
        driver = self.driver
        driver.get(self.base_url + "/index.php?route=common/home")
        driver.find_element_by_css_selector("i.fa.fa-user").click()
        driver.find_element_by_link_text("Register").click()
        driver.find_element_by_id("input-firstname").clear()
        driver.find_element_by_id("input-firstname").send_keys("Testing")
        driver.find_element_by_id("input-lastname").clear()
        driver.find_element_by_id("input-lastname").send_keys("Testing")
        driver.find_element_by_id("input-email").clear()
        driver.find_element_by_id("input-email").send_keys("Testing@Testing.Testing")
        driver.find_element_by_id("input-telephone").clear()
        driver.find_element_by_id("input-telephone").send_keys("0214521254")
        driver.find_element_by_id("input-address-1").clear()
        driver.find_element_by_id("input-address-1").send_keys("Testing 123")
        driver.find_element_by_id("input-city").clear()
        driver.find_element_by_id("input-city").send_keys("Testing")
        driver.find_element_by_id("input-postcode").clear()
        driver.find_element_by_id("input-postcode").send_keys("12345")
        Select(driver.find_element_by_id("input-zone")).select_by_visible_text("Aberdeenshire")
        driver.find_element_by_id("input-password").clear()
        driver.find_element_by_id("input-password").send_keys("Testing")
        driver.find_element_by_id("input-confirm").clear()
        driver.find_element_by_id("input-confirm").send_keys("Testing")
        driver.find_element_by_name("agree").click()
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_css_selector("i.fa.fa-user").click()
        driver.find_element_by_link_text("Logout").click()
        driver.get(self.base_url)
        driver.find_element_by_link_text("Phones & PDAs").click()
        driver.find_element_by_css_selector("div.button-group > button[type=\"button\"]").click()
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        driver.find_element_by_css_selector("a.btn.btn-primary").click()
        driver.find_element_by_id("input-email").clear()
        driver.find_element_by_id("input-email").send_keys("Testing@Testing.Testing")
        driver.find_element_by_id("input-password").clear()
        driver.find_element_by_id("input-password").send_keys("Testing")
        driver.find_element_by_id("button-login").click()
        driver.find_element_by_id("button-payment-address").click()
        driver.find_element_by_id("button-shipping-address").click()
        driver.find_element_by_id("button-shipping-method").click()
        driver.find_element_by_name("agree").click()
        driver.find_element_by_id("button-payment-method").click()
        driver.find_element_by_id("button-confirm").click()
        try: self.assertEqual("Your order has been placed!", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.get(self.base_url + "/index.php?route=account/account")
        driver.find_element_by_link_text("My Account").click()
        driver.find_element_by_link_text("Logout").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
