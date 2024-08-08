from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

from testcases.dev_BaseClass import dev_BaseClass


class StartWorkspace:
    def __init__(self, driver):
        self.driver = driver

    def process_workspaces(self):
        log = dev_BaseClass.getLogger()

        try:
            # Finding all rows in the tbody with role="rowgroup"
            rows = self.driver.find_elements(By.XPATH, "//tbody[@role='rowgroup']/tr")

            for row in rows:
                # Extract data-tip value
                data_tip = row.find_element(By.CLASS_NAME, "status-col-wrapper").get_attribute("data-tip")

                if "success" in data_tip.lower() or "progressing" in data_tip.lower():
                    continue

                elif "stopped" in data_tip.lower():
                    # Click on the action tooltip
                    action_tooltip = row.find_element(By.CLASS_NAME, "action-tooltip")
                    log.info("Clicked on the action tooltip.")
                    ActionChains(self.driver).move_to_element(action_tooltip).click().perform()
                    time.sleep(5)

                    # Click on the "Start" button
                    start_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Start')]")
                    log.info("Clicked on the 'Start' button.")
                    start_button.click()
                    time.sleep(5)

                    # Name for the current workspace
                    workspace_name_span = self.driver.find_element(By.XPATH, dev_BaseClass.WORKSPACE_VALUE_FETCH)
                    workspace_name = workspace_name_span.text.strip()
                    log.info(f"Workspace name: {workspace_name}")

                    workspace_name_input = self.driver.find_element(By.XPATH, "//input[@id='version-update']")
                    workspace_name_input.clear()
                    workspace_name_input.send_keys(workspace_name)
                    time.sleep(5)

                    delete_button_modal = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
                    delete_button_modal.click()
                    log.info("Clicked on the 'Start' button in the modal.")
                    time.sleep(10)

        except Exception as e:
            log.error(f"An error occurred: {e}")
