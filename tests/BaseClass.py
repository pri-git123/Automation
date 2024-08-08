import inspect
import logging
import subprocess

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseClass:
    # Login page
    EMAIL_INPUT = "(//form[@name='cognitoSignInForm']//input[@id='signInFormUsername'])[2]"
    PASSWORD_INPUT = "//form[@method='post']//input[@id='password']"
    SUBMIT_LOGIN_BUTTON = "//form[@method='post']//button[@id='submit-login']"

    # Home page
    SCIENCE_CLOUD_MODULE = "//a[@class='grid-item' and @href='/app/']/label[text()='Science Cloud']"

    # Workspace creation page
    ADD_NEW_BUTTON = "//a[contains(@class, 'btn-create') and contains(., 'Add New')]"
    WORKSPACE_TYPE_OPTION = lambda workspace_type: f'//div[text()="{workspace_type}"]'
    WORKSPACE_NAME_INPUT = "//form[@class='workspace-box-full-height']//input[@name='name']"
    SCROLL_TO_LAST_FORM = "//form[@class='workspace-box-full-height']"
    EDIT_BUTTON = "//form[@class='workspace-box-full-height']//button[@class='edit-button edit-labeled float-right bg-transparent']/div[@class='right-edit']"
    CPU_INPUT = "//div//input[@type='number' and @name='capacity.resources.cpu.value']"
    MEMORY_INPUT = "//div//input[@type='number' and @name='capacity.resources.memory.value']"
    CPU_UNIT_DROPDOWN = "//select[@name='capacity.resources.cpu.unit']/option[@value='m']"
    MEMORY_UNIT_DROPDOWN = "//select[@name='capacity.resources.memory.unit']/option[@value='Mi']"
    LAUNCH_BUTTON = "//button[contains(@class, 'btn-create') and contains(@type,'submit') ]"
    SUCCESS_MESSAGE = "//div[@class='success-message']"
    DELETE_ICON_XPATH = "//span[@data-tip='Delete']/span[@class='icon-delete black']"
    CONFIRM_ALERT_CLASS_NAME = 'react-confirm-alert'
    WORKSPACE_NAME_INPUT_ID = 'version-update'
    DELETE_BUTTON_MODAL_XPATH = "//button[contains(text(), 'Delete')]"
    Action_tooltip = "//span[@data-tip='Actions']"
    Stop_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Stop')]"
    WORKSPACE_VALUE_FETCH = "//div[@class='version-cluster pl-0']/span[@class='link-ellipsis']"
    Sharing_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Sharing')]"

    @staticmethod
    def switch_to_new_window(driver, main_window_handle):
        new_window_handle = WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

        # Switch to the new window
        all_window_handles = driver.window_handles
        new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
        driver.switch_to.window(new_window_handle)

    @pytest.fixture(scope="class")
    def setup_proxy(self):
        # Set the path to your private key file and SSH details
        ssh_key_path = '/Users/nishantchauhan/Downloads/private-browser.pem'
        ssh_host = 'ec2-user@34.199.223.179'
        local_port = 3128

        # Check if the port is already in use
        try:
            subprocess.run(["lsof", "-i", f":{local_port}"], check=True)
            print(f"Port {local_port} is already in use. Exiting.")
            exit()
        except subprocess.CalledProcessError:
            pass  # Port is not in use

        # Construct the SSH command
        ssh_command = f"ssh -ND {local_port} -v -i {ssh_key_path} {ssh_host}"

        ssh_process = subprocess.Popen(ssh_command, shell=True)
        time.sleep(30)

        # Create a WebDriver instance
        driver = webdriver.Firefox()
        yield driver

        # Teardown code
        driver.quit()
        ssh_process.terminate()
