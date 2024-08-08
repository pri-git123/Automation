import json
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from testcases.dev_BaseClass import dev_BaseClass


class PrivateLogin(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def module(self):
        log=self.getLogger()
        science_cloud_module = self.driver.find_element(By.XPATH, dev_BaseClass.SCIENCE_CLOUD_MODULE)
        science_cloud_module.click()
        time.sleep(10)
        main_window_handle = self.driver.current_window_handle
        dev_BaseClass.switch_to_new_window(self.driver, main_window_handle)
        time.sleep(10)
        log.info("Waiting for email input xpath to be located")

        # Read login credentials from JSON file
        with open("/Users/nishantchauhan/PycharmProjects/InvisblProject/testcases/login_credentials.json", "r") as file:
            login_data = json.load(file)

        element_email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dev_BaseClass.EMAIL_INPUT))
        )
        # self.driver.execute_script("arguments[0].scrollIntoView(true);", element_email)
        print("Before interacting with the element")
        element_email.send_keys(login_data["username"])
        time.sleep(5)
        print("After interacting with the element")

        element_password = self.driver.find_element(By.XPATH, dev_BaseClass.PASSWORD_INPUT)
        element_password.send_keys(login_data["password"])
        log.info("Submitting the login form")
        time.sleep(5)
        element_submit = self.driver.find_element(By.XPATH, dev_BaseClass.SUBMIT_LOGIN_BUTTON)
        element_submit.click()

        time.sleep(10)
        log.info("Login successful")



