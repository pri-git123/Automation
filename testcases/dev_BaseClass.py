import os

from selenium.common import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect
import logging


class dev_BaseClass:
    # EMAIL_INPUT = "//div[contains(@class, 'modal-content') and contains(@class, 'visible-md') and contains(@class, 'visible-lg')]//input[@id='signInFormUsername']"
    EMAIL_INPUT = "//div[contains(@class, 'visible-lg')]//input[@id='signInFormUsername']"
    PASSWORD_INPUT = "//div[contains(@class, 'visible-lg')]//input[@id='signInFormPassword']"
    SUBMIT_LOGIN_BUTTON = "//div[contains(@class, 'visible-lg')]//input[@name='signInSubmitButton']"
    ####### Private login inputs
    # EMAIL_INPUT = "//input[@id='login']"
    # PASSWORD_INPUT = "//form[@method='post']//input[@id='password']"
    # SUBMIT_LOGIN_BUTTON = "//form[@method='post']//button[@id='submit-login']"
    # SCIENCE_CLOUD_MODULE = "//a[@href='/datascience/']"
    SCIENCE_CLOUD_MODULE = "//a[label[text()='Datascience']]"
    V2_Quark_New = "//a[@href='/apps/quark/']"
    # v2_QUARK_MODULE = "//a[contains(@href, '/v2/') and contains(label/text(), 'Quark (v2)')]"
    ADD_NEW_BUTTON = "//span[normalize-space()='Add New']"
    WORKSPACE_TYPE_OPTION = lambda workspace_type: f'//div[text()="{workspace_type}"]'
    pipeline_xpath = lambda pipeline_name: f"(//div[contains(@class, 'catalog-card')]//div[contains(@class, 'card-title')]//div[contains(text(), '{pipeline_name}')])[1]"
    xpath_pipe = lambda pipeline_name: f"(//div[contains(@class, 'catalog-card')]//div[contains(text(), '{pipeline_name}')" \
        f"/ancestor::div[contains(@class, 'card-template')]//button[span[text()='Run']])[1]"
    Pipeline_NameInput = "//input[@name='name']"

    # PIPELINE_TYPE_OPTION = lambda pipeline_type: f'//h5[@class="card-label"]/div[text()="{pipeline_type}"]'
    WORKSPACE_NAME_INPUT = "//form[@class='workspace-box-full-height']//input[@name='name']"
    SCROLL_TO_LAST_FORM = "//form[@class='workspace-box-full-height']"
    EDIT_BUTTON = "//form[@class='workspace-box-full-height']//button[@class='edit-button edit-labeled float-right bg-transparent']/div[@class='right-edit']"
    CPU_INPUT = "//div//input[@type='number' and @name='capacity.resources.cpu.value']"
    MEMORY_INPUT = "//div//input[@type='number' and @name='capacity.resources.memory.value']"
    CPU_UNIT_DROPDOWN = "//select[@name='capacity.resources.cpu.unit']/option[@value='m']"
    MEMORY_UNIT_DROPDOWN = "//select[@name='capacity.resources.memory.unit']/option[@value='Mi']"
    # LAUNCH_BUTTON = "//button[contains(@class, 'btn-create') and contains(@type,'submit') ]"
    LAUNCH_BUTTON = "//div[@class='text-right p-2']/button/div[text()='Launch']"
    SUCCESS_MESSAGE = "//div[@class='success-message']"
    DELETE_ICON_XPATH = "//span[@class='icon' and @data-tip='Delete']"
    # DELETE_ICON_XPATH = "//span[@data-tip='Delete']/span[@class='icon-delete black']"
    CONFIRM_ALERT_CLASS_NAME = 'react-confirm-alert'
    WORKSPACE_NAME_INPUT_ID = 'version-update'
    DELETE_BUTTON_MODAL_XPATH = "//button[contains(text(), 'Delete')]"
    Action_tooltip = "//span[@data-tip='Actions']"
    Stop_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Stop')]"
    WORKSPACE_VALUE_FETCH = "//div[@class='version-cluster pl-0']/span[@class='link-ellipsis']"
    Start_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Start')]"
    Restart_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Restart')]"
    Sharing_button_xpath = "//div[@class='add_popup xxl']//span[contains(., 'Sharing')]"
    DELETE_WORKSPACE_BUTTON = "//span[@data-tip='Delete']/span[@class='icon-delete black']"
    Refreshing_button_xpath = "//span[@class='' and span[@class='refreshingIcon']]"
    Workspace_ICON = "//span[@class='menu-name' and text()='Workspaces']"
    Pipeline_tab = "//a[@data-tip='Pipelines']"
    Launchpad_tab = "//li[@class='react-tabs__tab' and text()='Launchpad']"
    PIPELINE_NAME_INPUT = "//div[@id='right-side-popup']//input[@name='name']"
    UPLOAD_FILE = "//div[@id='right-side-popup']//span[text()='Upload File']"

    @staticmethod
    def switch_to_new_window(driver, main_window_handle):
        new_window_handle = WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

        # Switch to the new window
        all_window_handles = driver.window_handles
        new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
        driver.switch_to.window(new_window_handle)

    @staticmethod
    def getLogger():
        # Get the directory of the current script
        current_directory = os.path.dirname(__file__)
        log_file_path = os.path.join(current_directory, 'logfile.log')

        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)

        fileHandler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)  # filehandler object
        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def take_screenshot(driver, filename):
        directory = "screenshots"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        try:
            driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
        except WebDriverException as e:
            print(f"Failed to capture screenshot: {e}")
