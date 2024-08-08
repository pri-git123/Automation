import time
import json
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from testcases.dev_BaseClass import dev_BaseClass

class TestWorkspace(dev_BaseClass):
    driver = None
    logged_in = False

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        # This fixture will be executed before and after each test method
        if not self.logged_in:
            self.driver = self.setup_driver()
            request.addfinalizer(self.quit_driver)
            self.login()
            self.logged_in = True

    def setup_driver(self):
        log = self.getLogger()
        log.info("Setting up the driver")
        options = Options()
        options.headless = False
        driver = webdriver.Chrome(options=options)
        return driver

    def quit_driver(self):
        if self.driver:
            # Uncomment the following line if you want to quit the browser after all tests are executed
            # self.driver.quit()
            pass

    def login(self):
        log = self.getLogger()
        log.info("Opening the login page")
        self.driver.get("https://dev2.gravity.invisibl.io/")
        time.sleep(10)
        self.driver.maximize_window()

        log.info("Clicking on the 'Science Cloud' module")
        science_cloud_module = self.driver.find_element(By.XPATH, dev_BaseClass.SCIENCE_CLOUD_MODULE)
        science_cloud_module.click()
        time.sleep(10)

        main_window_handle = self.driver.current_window_handle
        dev_BaseClass.switch_to_new_window(self.driver, main_window_handle)
        time.sleep(10)
        log.info("Waiting for email input xpath to be located")

        # Read login credentials from JSON file
        with open("/testcases/login_credentials.json", "r") as file:
            login_data = json.load(file)

        element_email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, dev_BaseClass.EMAIL_INPUT))
        )

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

    @pytest.mark.parametrize("workspace_data", json.load(
        open("/testcases/workspace_data.json"))["workspaces"])
    def test_create_workspace(self, workspace_data):
        log = self.getLogger()
        workspace_type = workspace_data["type"]
        workspace_name = workspace_data["name"]

        time.sleep(4)
        self.driver.find_element(By.XPATH, dev_BaseClass.ADD_NEW_BUTTON).click()
        time.sleep(5)
        self.driver.find_element(By.XPATH, f'//div[text()="{workspace_type}"]').click()
        time.sleep(5)
        # Use the provided workspace name
        self.driver.find_element(By.XPATH, dev_BaseClass.WORKSPACE_NAME_INPUT).send_keys(workspace_name)

        forms = self.driver.find_elements(By.XPATH, dev_BaseClass.SCROLL_TO_LAST_FORM)
        last_form = forms[-1]
        self.driver.execute_script("arguments[0].scrollIntoView();", last_form)
        edit_button = self.driver.find_element(By.XPATH, dev_BaseClass.EDIT_BUTTON)
        edit_button.click()
        input_cpu = self.driver.find_element(By.XPATH, dev_BaseClass.CPU_INPUT)
        input_cpu.clear()
        input_cpu.send_keys('252')
        input_memory = self.driver.find_element(By.XPATH, dev_BaseClass.MEMORY_INPUT)
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
        time.sleep(20)

    def test_stop_workspaces_from_json(self):
        log = self.getLogger()
        self.login()

        action_tips = self.driver.find_elements(By.XPATH, dev_BaseClass.Action_tooltip)

        for index, action_tip in enumerate(action_tips):
            # Click the action tip
            action_tip.click()
            time.sleep(5)

            # Find the stop button for the current workspace
            stop_button_xpath = f"({dev_BaseClass.Stop_button_xpath})[{index + 1}]"
            stop_button = self.driver.find_element(By.XPATH, stop_button_xpath)

            # Click the stop button
            stop_button.click()
            time.sleep(5)
            print("After the model content pop")
            time.sleep(4)

            try:
                # Name for the current workspace
                workspace_name_span = self.driver.find_element(By.XPATH, dev_BaseClass.WORKSPACE_VALUE_FETCH)
                workspace_name = workspace_name_span.text.strip()
                log.info("Stopping the workspace: %s", workspace_name)

                print("This is the workspace name: ", workspace_name)
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
