from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class RefreshPage:
    def __init__(self, driver):
        self.driver = driver

    def click_second_option(self):
        dropdown_element = self.driver.find_element(By.CLASS_NAME, "css-1wy0on6")

        # Click on the dropdown element to reveal the options
        dropdown_element.click()

        # Wait for the dropdown options to be visible
        dropdown_options = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-tlfecz-indicatorContainer")))

        # Iterate through the options and find the "10secs" option
        for option in dropdown_options:
            if option.text == "10secs":
                # Scroll to the option
                ActionChains(self.driver).move_to_element(option).perform()

                # Click on the "10secs" option
                option.click()
                break
