# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
from mySelect import Select

class Test7(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(30)
        self.base_url = "http://mys01.fit.vutbr.cz:8012/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_7(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Phones & PDAs").click()
        driver.find_element_by_css_selector("div.button-group > button[type=\"button\"]").click()
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        driver.find_element_by_css_selector("a.btn.btn-primary").click()
        driver.find_element_by_xpath("(//input[@name='account'])[2]").click()
        driver.find_element_by_xpath("//div[@id='collapse-checkout-option']/div/div/div/div[2]/label").click()
        driver.find_element_by_id("button-account").click()
        driver.find_element_by_id("input-payment-firstname").clear()
        driver.find_element_by_id("input-payment-firstname").send_keys("Test")
        driver.find_element_by_id("input-payment-lastname").clear()
        driver.find_element_by_id("input-payment-lastname").send_keys("Test")
        driver.find_element_by_id("input-payment-email").clear()
        driver.find_element_by_id("input-payment-email").send_keys("Test@Test.Test")
        driver.find_element_by_id("input-payment-telephone").clear()
        driver.find_element_by_id("input-payment-telephone").send_keys("0214521254")
        driver.find_element_by_id("input-payment-address-1").clear()
        driver.find_element_by_id("input-payment-address-1").send_keys("Test 123")
        driver.find_element_by_id("input-payment-city").clear()
        driver.find_element_by_id("input-payment-city").send_keys("Test")
        driver.find_element_by_id("input-payment-postcode").clear()
        driver.find_element_by_id("input-payment-postcode").send_keys("12345")
        Select(driver.find_element_by_id("input-payment-zone")).select_by_visible_text("Berkshire")
        driver.find_element_by_id("button-guest").click()
        driver.find_element_by_id("button-shipping-method").click()
        time.sleep(5)
        driver.find_element_by_name("agree").click()
        driver.find_element_by_id("button-payment-method").click()
        driver.find_element_by_id("button-confirm").click()
        try: self.assertEqual("Your order has been placed!", driver.find_element_by_css_selector("h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
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
