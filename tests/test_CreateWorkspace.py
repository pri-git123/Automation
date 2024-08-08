import subprocess
import time
from select import select
import json
import pytest
from selenium.common import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import re
from tests.BaseClass import BaseClass


@pytest.mark.usefixtures("setup_proxy")
class TestWorkspace(BaseClass):
    driver = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, setup_proxy):
        # This fixture will be executed before and after each test method
        self.driver = setup_proxy
        yield
        self.driver.quit()

    def login(self):
            log = self.getLogger()
            log.info("Opening the login page")
            self.driver.get("https://regn.invisibl.io/")
            self.driver.maximize_window()

            log.info("Clicking on the 'Science Cloud' module")
            science_cloud_module = self.driver.find_element(By.XPATH, BaseClass.SCIENCE_CLOUD_MODULE)
            science_cloud_module.click()

            main_window_handle = self.driver.current_window_handle
            BaseClass.switch_to_new_window(self.driver, main_window_handle)

            log.info("Entering login credentials")

            # Read login credentials from JSON file
            with open("/Users/nishantchauhan/PycharmProjects/InvisblProject/tests/login_credentials.json", "r") as file:
                login_data = json.load(file)

            log.info("After Reading from json")

            element_email = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, BaseClass.EMAIL_INPUT))
            )
            element_email.send_keys(login_data["email"])

            element_password = self.driver.find_element(By.XPATH, BaseClass.PASSWORD_INPUT)
            element_password.send_keys(login_data["password"])

            log.info("Submitting the login form")
            time.sleep(5)
            self.driver.find_element(By.ID, 'submit-login').click()
            time.sleep(10)
            log.info("Login successful")


    def test_login(self):
        self.login()


    @pytest.mark.parametrize("workspace_data", json.load(open("/Users/nishantchauhan/PycharmProjects/InvisblProject/tests/workspace_data.json"))["workspaces"])
    def test_create_workspace(self, workspace_data):
        log =self.getLogger()
        self.login()
        workspace_type = workspace_data["type"]
        workspace_name = workspace_data["name"]

        time.sleep(4)
        self.driver.find_element(By.XPATH, BaseClass.ADD_NEW_BUTTON).click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, f'//div[text()="{workspace_type}"]').click()
        time.sleep(5)
        # Use the provided workspace name
        self.driver.find_element(By.XPATH, BaseClass.WORKSPACE_NAME_INPUT).send_keys(workspace_name)

        forms = self.driver.find_elements(By.XPATH, BaseClass.SCROLL_TO_LAST_FORM)
        last_form = forms[-1]
        self.driver.execute_script("arguments[0].scrollIntoView();", last_form)
        edit_button = self.driver.find_element(By.XPATH, BaseClass.EDIT_BUTTON)
        edit_button.click()
        input_cpu = self.driver.find_element(By.XPATH, BaseClass.CPU_INPUT)
        input_cpu.clear()
        input_cpu.send_keys('252')
        input_memory = self.driver.find_element(By.XPATH, BaseClass.MEMORY_INPUT)
        input_memory.clear()
        input_memory.send_keys('250')
        self.driver.find_element(By.XPATH, "//select[@name='capacity.resources.cpu.unit']/option[@value='m']")
        dropdown_cpu = Select(self.driver.find_element(By.NAME, "capacity.resources.cpu.unit"))
        dropdown_cpu.select_by_value('m')
        dropdown_memory = Select(self.driver.find_element(By.NAME, "capacity.resources.memory.unit"))
        dropdown_memory.select_by_value("Mi")
        self.driver.find_element(By.XPATH,
                                 "//button[contains(@class, 'edit-button') and contains(@class, 'edit-labeled')]").click()
        # Click on launch
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(@class, 'btn-create') and contains(@type,'submit')]"))).click()
        time.sleep(5)

    def test_stop_workspaces_from_json(self):
        log = self.getLogger()
        self.login()

        action_tips = self.driver.find_elements(By.XPATH, BaseClass.Action_tooltip)

        for index, action_tip in enumerate(action_tips):
            # Click the action tip
            action_tip.click()
            time.sleep(5)

            # Find the stop button for the current workspace
            stop_button_xpath = f"({BaseClass.Stop_button_xpath})[{index + 1}]"
            stop_button = self.driver.find_element(By.XPATH, stop_button_xpath)

            # Click the stop button
            stop_button.click()
            time.sleep(5)
            print("After the model content pop")
            time.sleep(4)

            try:
                #  name for the current workspace
                workspace_name_span = self.driver.find_element(By.XPATH, BaseClass.WORKSPACE_VALUE_FETCH)
                workspace_name = workspace_name_span.text.strip()
                log.info("Stopping the workspace: %s", workspace_name)

                print("this is the workspace name: ", workspace_name)
                time.sleep(5)

                workspace_name_input = self.driver.find_element(By.XPATH, "//input[@id='version-update']")
                workspace_name_input.clear()
                workspace_name_input.send_keys(workspace_name)
                time.sleep(5)

                delete_button_modal = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Stop')]")
                delete_button_modal.click()
                time.sleep(10)

                # Optionally, wait for some time to ensure the workspace is deleted successfully
                self.driver.implicitly_wait(3)

            except NoSuchElementException as e:
                print(f"Error locating workspace name: {e}")

    def test_Refresh(self):
        self.login()
        self.driver.find_element(By.XPATH,"//div[@class='css-qc6sy-singleValue' and text()='YourText']").click()


    def test_Delete_workspace(self):
        log = self.getLogger()
        self.login()
        # Find all delete buttons for workspaces
        delete_buttons = self.driver.find_elements(By.XPATH,
                                                   "//span[@data-tip='Delete']/span[@class='icon-delete black']")

        for delete_button in delete_buttons:
            delete_button.click()

            wait = WebDriverWait(self.driver, 20)
            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'react-confirm-alert')))
            time.sleep(10)

            try:

                workspace_name_span = modal.find_element(By.XPATH,
                                                         ".//div[contains(@class, 'version-cluster')]/span[@class='link-ellipsis']")
                workspace_name = workspace_name_span.text.strip()
                log.info("Deleting workspace: %s", workspace_name)

                print("this is the workspace name: ", workspace_name)
                time.sleep(5)
                workspace_name_input = modal.find_element(By.XPATH, "//input[@id='version-update']")

                workspace_name_input.clear()
                workspace_name_input.send_keys(workspace_name)
                time.sleep(5)

                delete_button_modal = modal.find_element(By.XPATH, "//button[contains(text(), 'Delete')]")
                delete_button_modal.click()

                # Optionally, wait for some time to ensure the workspace is deleted successfully
                self.driver.implicitly_wait(3)

            except NoSuchElementException as e:
                print(f"Error locating workspace name: {e}")
