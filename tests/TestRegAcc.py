from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestRegAcc(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"
        self.verificationErrors = []
        self.accept_next_alert = true
    
    def test_reg_acc(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("#c35114320 > ol.context-line > li > pre").click()
        driver.find_element_by_link_text("Regsiter").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("abc")
        driver.find_element_by_id("id_full_name").clear()
        driver.find_element_by_id("id_full_name").send_keys("abc")
        driver.find_element_by_id("id_email1").clear()
        driver.find_element_by_id("id_email1").send_keys("a@gmail.com")
        driver.find_element_by_id("id_email2").clear()
        driver.find_element_by_id("id_email2").send_keys("a@gmail.com")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("abc")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("abc")
        driver.find_element_by_name("Submit").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
