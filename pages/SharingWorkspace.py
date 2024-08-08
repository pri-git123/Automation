from selenium.webdriver.common.by import By
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testcases.dev_BaseClass import dev_BaseClass

class SharingWorkspace(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def sharing_workspaces(self):
        log = dev_BaseClass.getLogger()
        # Find all action tips representing different workspaces
        action_tips = self.driver.find_elements(By.XPATH, dev_BaseClass.Action_tooltip)

        # Iterate through each action tip (workspace)
        for index, action_tip in enumerate(action_tips):
            try:
                # Click the action tip
                action_tip.click()
                log.info(f"Clicked on the action tip for workspace {index + 1}.")
                time.sleep(5)

                sharing_button_xpath = f"({dev_BaseClass.Sharing_button_xpath})[{index + 1}]"

                # Attempt to find the sharing button
                sharing_button = self.driver.find_element(By.XPATH, sharing_button_xpath)

                # Click the sharing button
                sharing_button.click()
                log.info("Clicked on the sharing button.")
                time.sleep(2)

                # Wait for the "Please Select" option to be clickable
                please_select_div = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Please Select']"))
                )

                # Click on the "Please Select" option
                please_select_div.click()
                log.info("Clicked on the 'Please Select' option.")

                # Select 'deepa' from the dropdown
                deepa_option_xpath = "//div[@id='react-select-3-option-2']"
                deepa_option = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, deepa_option_xpath))
                )
                deepa_option.click()
                log.info("Selected 'deepa' from the dropdown.")

                # Find and click the "Copy" button
                time.sleep(5)
                copy_button_xpath = "//button[contains(@class, 'btn-copy')]"
                copy_button = self.driver.find_element(By.XPATH, copy_button_xpath)
                copy_button.click()
                log.info("Clicked on the 'Copy' button.")

                # Find and click the "Submit" button
                time.sleep(5)
                submit_button_xpath = "//button[@type='submit' and contains(@class, 'btn-create')]"
                submit_button = self.driver.find_element(By.XPATH, submit_button_xpath)
                submit_button.click()
                log.info("Clicked on the 'Submit' button.")

            except NoSuchElementException as e:
                log.error(f"Element not found: {e}")
                continue  # Move to the next action tip
            except TimeoutException as te:
                log.error(f"Timeout occurred: {te}")
                continue  # Move to the next action tip
            except Exception as ex:
                log.error(f"An error occurred: {ex}")
                continue  # Move to the next action tip
