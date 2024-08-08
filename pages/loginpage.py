import json
import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from testcases.dev_BaseClass import dev_BaseClass


class LoginPage(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def module(self):
        log = self.getLogger()  # Get logger instance
        try:
            science_cloud_module = self.driver.find_element(By.XPATH, dev_BaseClass.V2_Quark_New)
            science_cloud_module.click()

            log.info("Clicked on 'Science Cloud' module.")
            time.sleep(10)

            main_window_handle = self.driver.current_window_handle
            dev_BaseClass.switch_to_new_window(self.driver, main_window_handle)
            log.info("Switched to new window.")
            time.sleep(10)

            log.info("Waiting for email input element to be located.")
            # Read login credentials from JSON file
            with open("/Users/nishantchauhan/PycharmProjects/InvisblProject/testcases/login_credentials.json",
                      "r") as file:
                login_data = json.load(file)

            element_email = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, dev_BaseClass.EMAIL_INPUT))
            )
            element_email.send_keys(login_data["username"])
            log.info("Entered email address.")

            element_password = self.driver.find_element(By.XPATH, dev_BaseClass.PASSWORD_INPUT)
            element_password.send_keys(login_data["password"])
            log.info("Entered password.")

            element_submit = self.driver.find_element(By.XPATH, dev_BaseClass.SUBMIT_LOGIN_BUTTON)
            element_submit.click()
            log.info("Clicked on 'Submit' button.")
            time.sleep(10)

            log.info("Login successful.")
        except Exception as e:
            log.error(f"Failed to log in. Error: {str(e)}")
            self.take_screenshot(self.driver, "login_error.png")
            raise e
