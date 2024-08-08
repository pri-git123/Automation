import json
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testcases.dev_BaseClass import dev_BaseClass


class ConnectWorkspace(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def connect_demoprotein(self):
        log = self.getLogger()

        # Click on the connect button
        try:
            connect_button = self.driver.find_element(By.XPATH, "//span[@data-tip='Connect']/span[@class='icon-connect black']")
            connect_button.click()
            log.info("Clicked on the 'Connect' button.")
        except NoSuchElementException:
            log.error("Connect button not found.")
            return

        # Switch to the new window
        main_window_handle = self.driver.current_window_handle
        dev_BaseClass.switch_to_new_window(self.driver, main_window_handle)
        log.info("Switched to the new window.")

        # Read login credentials from JSON file
        try:
            with open("/Users/nishantchauhan/PycharmProjects/InvisblProject/tests/login_credentials.json", "r") as file:
                login_data = json.load(file)
        except FileNotFoundError:
            log.error("Login credentials file not found.")
            return

        # Enter login credentials
        try:
            element_email = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, dev_BaseClass.EMAIL_INPUT))
            )
            element_email.send_keys(login_data["username"])
            log.info("Entered username.")

            element_password = self.driver.find_element(By.XPATH, dev_BaseClass.PASSWORD_INPUT)
            element_password.send_keys(login_data["password"])
            log.info("Entered password.")

            element_submit = self.driver.find_element(By.XPATH, dev_BaseClass.SUBMIT_LOGIN_BUTTON)
            element_submit.click()
            log.info("Clicked on the 'Submit' button.")
        except NoSuchElementException:
            log.error("Login form elements not found.")
            return
        except TimeoutException:
            log.error("Timed out while waiting for login form elements.")
            return

        time.sleep(10)
        log.info("Login successful.")
