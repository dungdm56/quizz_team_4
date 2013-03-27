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
        driver.get(self.base_url + "/login/")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("naruto")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_link_text("Create Class").click()
        driver.find_element_by_id("id_class_name").clear()
        driver.find_element_by_id("id_class_name").send_keys("K56-CA-Trial")
        driver.find_element_by_id("id_number_students").clear()
        driver.find_element_by_id("id_number_students").send_keys("40")
        driver.find_element_by_id("id_teacher_name").clear()
        driver.find_element_by_id("id_teacher_name").send_keys("Võ Anh Hưng")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_link_text("click here").click()
        driver.find_element_by_xpath("(//a[contains(text(),'admin')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'admin')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'admin')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'admin')])[2]").click()
        driver.find_element_by_xpath("(//a[contains(text(),'admin')])[2]").click()
    
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
