import subprocess
import time
from select import select

import pytest
from selenium.common import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


@pytest.mark.usefixtures("setup_proxy")
class TestWorkspace:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, setup_proxy):
        # This fixture will be executed before and after each test method
        self.driver = setup_proxy
        yield
        #self.driver.quit()

    def login(self):
        self.driver.get("https://regn.invisibl.io/")
        science_cloud_module = self.driver.find_element(By.XPATH, "//a[@class='grid-item' and @href='/app/']/label[text()='Science Cloud']")
        science_cloud_module.click()
        main_window_handle = self.driver.current_window_handle
        new_window_handle = WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))

        # Switch to the new window
        all_window_handles = self.driver.window_handles
        new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
        self.driver.switch_to.window(new_window_handle)

        ##credentials
        email_xpath = "//form[@method='post']//input[@id='login']"
        password_xpath = "//form[@method='post']//input[@id='password']"

        element_email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, email_xpath))
        )
        element_email.send_keys("raghuraman.balachand@regeneron.com")

        element_password = self.driver.find_element(By.XPATH, password_xpath)
        element_password.send_keys("jh2348fijk34b59sdf4kj")
        time.sleep(5)
        self.driver.find_element(By.ID, 'submit-login').click()
        time.sleep(20)

    def test_login(self):
        self.login()

    @pytest.mark.parametrize("workspace_type", ["Basic JupyterLab", "Admin Terminal",'(Demo) Protein Folding using Alphafold2'])
    def test_create_workspace(self, workspace_type):

        self.login()

        time.sleep(4)
        self.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-create') and contains(., 'Add New')]").click()

        #########Basic Jupyetr

        time.sleep(10)
        self.driver.find_element(By.XPATH, f'//div[text()="{workspace_type}"]').click()

        time.sleep(10)
        #self.driver.find_element(By.XPATH, "//form[@class='workspace-box-full-height']//input[@name='name']").send_keys(
          #  "test01")
        self.driver.find_element(By.XPATH, "//form[@class='workspace-box-full-height']//input[@name='name']").send_keys("work-basic ")

        forms = self.driver.find_elements(By.XPATH, "//form[@class='workspace-box-full-height']")

        last_form = forms[-1]
        self.driver.execute_script("arguments[0].scrollIntoView();", last_form)

        # Find and click the Edit button
        edit_button_xpath = "//form[@class='workspace-box-full-height']//button[@class='edit-button edit-labeled float-right bg-transparent']/div[@class='right-edit']"
        edit_button = self.driver.find_element(By.XPATH, edit_button_xpath)
        edit_button.click()
        #####cpu inputs
        # input_element_xpath = "//div[@class='col-6']//input[@class='form-control' and @type='number' and @name='capacity.resources.cpu.value']"
        input_cpu_xpath = "//div//input[@type='number' and @name='capacity.resources.cpu.value']"
        input_cpu = self.driver.find_element(By.XPATH, input_cpu_xpath)
        input_cpu.clear()
        input_cpu.send_keys('252')
        ### values for memeory
        input_memory_xpath = "//div//input[@type='number' and @name='capacity.resources.memory.value']"
        input_memory = self.driver.find_element(By.XPATH, input_memory_xpath)
        input_memory.clear()
        input_memory.send_keys('250')
        self.driver.find_element(By.XPATH, "//select[@name='capacity.resources.cpu.unit']/option[@value='m']")
        # Clear the existing value
        # Enter a new value (replace 'new_value' with the desired value)
        dropdown_cpu = Select(self.driver.find_element(By.NAME, "capacity.resources.cpu.unit"))
        dropdown_cpu.select_by_value('m')
        dropdown_memory = Select(self.driver.find_element(By.NAME, "capacity.resources.memory.unit"))
        dropdown_memory.select_by_value("Mi")
        self.driver.find_element(By.XPATH,"//button[contains(@class, 'edit-button') and contains(@class, 'edit-labeled')]").click()
        self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-create') and contains(@type,'submit') ]").click()


