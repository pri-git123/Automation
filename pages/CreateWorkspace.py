import json
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testcases.dev_BaseClass import dev_BaseClass


class CreateWorkspace(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def create(self, workspace_data):
        time.sleep(5)

        log = self.getLogger()  # Get logger instance
        try:
            workspace_type = workspace_data["type"]
            workspace_name = workspace_data["name"]

            # Click on Workspa

            log.info("Starting workspace creation process...")
            time.sleep(4)

            self.driver.find_element(By.XPATH, dev_BaseClass.ADD_NEW_BUTTON).click()
            log.info("Clicked on 'Add New' button.")
            time.sleep(5)
            self.driver.find_element(By.XPATH, f'//div[text()="{workspace_type}"]').click()
            log.info(f"Selected workspace type: {workspace_type}")
            time.sleep(10)
            self.driver.find_element(By.XPATH, dev_BaseClass.WORKSPACE_NAME_INPUT).send_keys(workspace_name)
            log.info(f"Entered workspace name: {workspace_name}")

            forms = self.driver.find_elements(By.XPATH, dev_BaseClass.SCROLL_TO_LAST_FORM)
            last_form = forms[-1]
            self.driver.execute_script("arguments[0].scrollIntoView();", last_form)
            edit_button = self.driver.find_element(By.XPATH, dev_BaseClass.EDIT_BUTTON)
            edit_button.click()
            log.info("Clicked on 'Edit' button.")

            input_cpu = self.driver.find_element(By.XPATH, dev_BaseClass.CPU_INPUT)
            input_cpu.clear()
            input_cpu.send_keys('150')
            log.info("Entered CPU value: 150")

            input_memory = self.driver.find_element(By.XPATH, dev_BaseClass.MEMORY_INPUT)
            input_memory.clear()
            input_memory.send_keys('152')
            log.info("Entered memory value: 152")

            dropdown_cpu = Select(self.driver.find_element(By.NAME, "capacity.resources.cpu.unit"))
            dropdown_cpu.select_by_value('m')
            log.info("Selected CPU unit: m")

            dropdown_memory = Select(self.driver.find_element(By.NAME, "capacity.resources.memory.unit"))
            dropdown_memory.select_by_value("Mi")
            log.info("Selected memory unit: Mi")

            self.driver.find_element(By.XPATH,
                                     "//button[contains(@class, 'edit-button') and contains(@class, 'edit-labeled')]").click()
            log.info("Clicked on 'Edit' button.")
            time.sleep(5)

            # Click on launch
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, dev_BaseClass.LAUNCH_BUTTON))).click()
            log.info("Clicked on 'Launch' button.")
            time.sleep(10)

            log.info(f"Workspace '{workspace_name}' created successfully.")
        except Exception as e:
            log.error(f"Failed to create workspace '{workspace_name}'. Error: {str(e)}")
            self.take_screenshot(self.driver, f"create_workspace_error_{workspace_name}.png")
            raise e
