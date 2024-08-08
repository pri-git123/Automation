from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from testcases.dev_BaseClass import dev_BaseClass


class RestartWorkspace:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_success_workspaces(self):
        log = dev_BaseClass.getLogger()
        try:
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//tbody[@role='rowgroup']/tr[contains(@class, 'success')]")
                )
            )
            log.info("Successfully waited for success workspaces.")
        except Exception as e:
            log.error(f"An error occurred while waiting for success workspaces: {e}")

    def restart_workspace_by_row(self, row):
        log = dev_BaseClass.getLogger()
        try:
            data_tip = row.find_element(By.CLASS_NAME, "status-col-wrapper").get_attribute("data-tip")

            if "stopped" in data_tip.lower() or "Deleting" in data_tip.lower():
                return

            elif "success" in data_tip.lower() or "Progressing" in data_tip.lower():
                # Click on the action tooltip
                action_tooltip = row.find_element(By.CLASS_NAME, "action-tooltip")
                ActionChains(self.driver).move_to_element(action_tooltip).click().perform()
                time.sleep(5)

                # Click on the "Stop" button
                stop_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Restart')]")
                stop_button.click()

                # Name for the current workspace
                workspace_name_span = self.driver.find_element(By.XPATH, dev_BaseClass.WORKSPACE_VALUE_FETCH)
                workspace_name = workspace_name_span.text.strip()
                log.info(f"This is the workspace name: {workspace_name}")
                time.sleep(5)

                workspace_name_input = self.driver.find_element(By.XPATH, "//input[@id='version-update']")
                workspace_name_input.clear()
                workspace_name_input.send_keys(workspace_name)
                time.sleep(5)

                restart_button_modal = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Restart')]")
                restart_button_modal.click()
                time.sleep(5)

        except Exception as e:
            log.error(f"An error occurred while stopping workspace: {e}")

    def restart_workspaces(self):
        log = dev_BaseClass.getLogger()
        try:
            self.wait_for_success_workspaces()

            # Click the "Refresh" button after the wait
            refresh_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'refreshingIcon')]")
            refresh_button.click()
            time.sleep(5)
            log.info("Clicked the 'Refresh' button.")

            # Find all rows in the tbody with role="rowgroup"
            rows = self.driver.find_elements(By.XPATH, "//tbody[@role='rowgroup']/tr")

            for row in rows:
                self.restart_workspace_by_row(row)

        except Exception as e:
            log.error(f"An error occurred: {e}")
