# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
from mySelect import Select

class Test5(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(30)
        self.base_url = "http://mys01.fit.vutbr.cz:8012/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_5(self):
        driver = self.driver
        driver.get(self.base_url + "/admin/")
        driver.find_element_by_id("input-username").clear()
        driver.find_element_by_id("input-username").send_keys("admin")
        driver.find_element_by_id("input-password").clear()
        driver.find_element_by_id("input-password").send_keys("admin")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_id("button-menu").click()
        driver.find_element_by_link_text("Marketing").click()
        driver.find_element_by_link_text("Coupons").click()
        driver.find_element_by_xpath("//form[@id='form-coupon']/div/table/tbody/tr[2]/td[8]/a").click()
        Select(driver.find_element_by_id("input-status")).select_by_visible_text("Enabled")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Phones & PDAs").click()
        driver.find_element_by_css_selector("div.button-group > button[type=\"button\"]").click()
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        driver.find_element_by_xpath(".//*[@id='accordion']/div[1]/div[1]/h4/a/i").click()
        driver.find_element_by_id("input-coupon").clear()
        driver.find_element_by_id("input-coupon").send_keys("1111")
        driver.find_element_by_id("button-coupon").click()
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-success"))
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
