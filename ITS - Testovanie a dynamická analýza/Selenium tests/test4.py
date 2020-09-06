# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
from mySelect import Select

class Test4(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(30)
        self.base_url = "http://mys01.fit.vutbr.cz:8012/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_4(self):
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        driver.find_element_by_id("input-username").clear()
        driver.find_element_by_id("input-username").send_keys("admin")
        driver.find_element_by_id("input-password").clear()
        driver.find_element_by_id("input-password").send_keys("admin")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_css_selector("#sale > a.parent").click()
        driver.find_element_by_link_text("Gift Vouchers").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Gift Vouchers')])[2]").click()
        driver.find_element_by_css_selector("i.fa.fa-plus").click()
        driver.find_element_by_id("input-code").clear()
        driver.find_element_by_id("input-code").send_keys("gift")
        driver.find_element_by_id("input-from-name").clear()
        driver.find_element_by_id("input-from-name").send_keys("Test")
        driver.find_element_by_id("input-from-email").clear()
        driver.find_element_by_id("input-from-email").send_keys("Test@Test.Test")
        driver.find_element_by_id("input-to-name").clear()
        driver.find_element_by_id("input-to-name").send_keys("Test")
        driver.find_element_by_id("input-to-email").clear()
        driver.find_element_by_id("input-to-email").send_keys("Test@Test.Test")
        driver.find_element_by_id("input-message").clear()
        driver.find_element_by_id("input-message").send_keys("Test")
        driver.find_element_by_id("input-amount").clear()
        driver.find_element_by_id("input-amount").send_keys("1")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Phones & PDAs").click()
        driver.find_element_by_css_selector("div.button-group > button[type=\"button\"]").click()
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        driver.find_element_by_xpath(".//*[@id='accordion']/div[3]/div[1]/h4/a/i").click()
        driver.find_element_by_id("input-voucher").clear()
        driver.find_element_by_id("input-voucher").send_keys("gift")
        driver.find_element_by_id("button-voucher").click()
        driver.find_element_by_css_selector("a.btn.btn-primary").click()
        driver.find_element_by_xpath("(//input[@name='account'])[2]").click()
        driver.find_element_by_xpath("//div[@id='collapse-checkout-option']/div/div/div/div[2]/label").click()
        driver.find_element_by_id("button-account").click()
        driver.find_element_by_id("input-payment-firstname").clear()
        driver.find_element_by_id("input-payment-firstname").send_keys("Test123")
        driver.find_element_by_id("input-payment-lastname").clear()
        driver.find_element_by_id("input-payment-lastname").send_keys("Test123")
        driver.find_element_by_id("input-payment-email").clear()
        driver.find_element_by_id("input-payment-email").send_keys("Test123@Test.com")
        driver.find_element_by_id("input-payment-telephone").clear()
        driver.find_element_by_id("input-payment-telephone").send_keys("0123254165")
        driver.find_element_by_id("input-payment-address-1").clear()
        driver.find_element_by_id("input-payment-address-1").send_keys("Testing 123")
        driver.find_element_by_id("input-payment-city").clear()
        driver.find_element_by_id("input-payment-city").send_keys("Testing")
        driver.find_element_by_id("input-payment-postcode").clear()
        driver.find_element_by_id("input-payment-postcode").send_keys("12345")
        Select(driver.find_element_by_id("input-payment-country")).select_by_visible_text("Turkmenistan")
        Select(driver.find_element_by_id("input-payment-zone")).select_by_visible_text("Ahal Welayaty")
        driver.find_element_by_id("button-guest").click()
        driver.find_element_by_id("button-shipping-method").click()
        driver.find_element_by_name("agree").click()
        driver.find_element_by_id("button-payment-method").click()
        driver.find_element_by_id("button-confirm").click()
        driver.find_element_by_link_text("Phones & PDAs").click()
        driver.find_element_by_css_selector("div.button-group > button[type=\"button\"]").click()
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        driver.find_element_by_xpath(".//*[@id='accordion']/div[3]/div[1]/h4/a/i").click()
        driver.find_element_by_id("input-voucher").clear()
        driver.find_element_by_id("input-voucher").send_keys("gift")
        driver.find_element_by_id("button-voucher").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-danger"))
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
