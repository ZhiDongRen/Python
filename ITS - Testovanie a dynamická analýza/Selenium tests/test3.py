# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
from mySelect import Select

class Test3(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(30)
        self.base_url = "http://mys01.fit.vutbr.cz:8012/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_3(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Components").click()
        time.sleep(1)
        driver.find_element_by_link_text("Monitors (2)").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        time.sleep(1)
        driver.find_element_by_css_selector("i.fa.fa-shopping-cart").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='content']/form/div/table/tbody/tr/td[4]/div/input").clear()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[@id='content']/form/div/table/tbody/tr/td[4]/div/input").send_keys("10000000")
        time.sleep(1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        time.sleep(1)
        try: self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "div.alert.alert-danger"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        time.sleep(1)
        driver.find_element_by_css_selector("span.input-group-btn > button.btn.btn-danger").click()
        # ERROR: Caught exception [unknown command []]
    
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
