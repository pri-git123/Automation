import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from testcases.dev_BaseClass import dev_BaseClass

class DeleteWorkspace(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def delete_workspace(self):
        log = self.getLogger()  # Initialize logger

        while True:
            delete_buttons = self.driver.find_elements(By.XPATH, "//span[@class='icon' and @data-tip='Delete']")

            if not delete_buttons:
                log.info("No more workspaces to delete.")
                break

            for delete_button in delete_buttons:
                try:
                    if not delete_button.is_enabled():
                        log.warning("Delete button is disabled. Skipping to the next workspace.")
                        continue

                    delete_button.click()

                    wait = WebDriverWait(self.driver, 20)
                    modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'react-confirm-alert')))
                    time.sleep(10)

                    workspace_name_span = modal.find_element(By.XPATH,
                                                             ".//div[contains(@class, 'version-cluster')]/span[@class='link-ellipsis']")
                    workspace_name = workspace_name_span.text.strip()
                    log.info("Deleting workspace: %s", workspace_name)

                    print("This is the workspace name: ", workspace_name)
                    time.sleep(5)
                    workspace_name_input = modal.find_element(By.XPATH, "//input[@id='version-update']")

                    workspace_name_input.clear()
                    workspace_name_input.send_keys(workspace_name)
                    time.sleep(5)

                    delete_button_modal = modal.find_element(By.XPATH, "//button[contains(text(), 'Delete')]")
                    delete_button_modal.click()
                    time.sleep(4)

                    self.driver.implicitly_wait(3)

                except NoSuchElementException as e:
                    log.error(f"Error locating workspace name: {e}")

            # Refresh
