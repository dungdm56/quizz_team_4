from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestCreateClass(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/create_class/"
        self.verificationErrors = []
        self.accept_next_alert = true
    
    def test_create_class(self):
        driver = self.driver
        driver.get(self.base_url + "/create_class/")
        driver.find_element_by_id("id_class_name").clear()
        driver.find_element_by_id("id_class_name").send_keys("K56-CA-Trial")
        driver.find_element_by_id("id_number_students").clear()
        driver.find_element_by_id("id_number_students").send_keys("50")
        driver.find_element_by_id("id_teacher_name").clear()
        driver.find_element_by_id("id_teacher_name").send_keys("FinalDevil")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_id("id_class_name").clear()
        driver.find_element_by_id("id_class_name").send_keys("K56-CA-Trial-1")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_link_text("click here").click()
    
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
