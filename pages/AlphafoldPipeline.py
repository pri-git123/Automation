import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testcases.dev_BaseClass import dev_BaseClass


class AlphafoldPipeline(dev_BaseClass):
    def __init__(self, driver):
        self.driver = driver

    def create_pipeline(self, pipeline_data):
        log = self.getLogger()
        pipeline_name = pipeline_data.get('selected_pipeline')
        job_name = pipeline_data.get('name')
        file_path = pipeline_data.get('file_path')

        # Verify file path
        if not os.path.exists(file_path):
            log.error(f"File path does not exist: {file_path}")
            return

        try:
            time.sleep(6)

            # Find and click the pipeline run button
            xpath_pipe = f"(//div[contains(@class, 'catalog-card')]//div[contains(text(), '{pipeline_name}')]" \
                         f"/ancestor::div[contains(@class, 'card-template')]//button[span[text()='Run']])[1]"
            log.info(f"Clicking pipeline run button: {xpath_pipe}")
            run_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_pipe))
            )
            run_button.click()
            time.sleep(4)

            # Input job name
            xpath_jobname = ("//form[@class='workspace-box-full-height create-job-form']//label[text()='Name']"
                             "/following-sibling::div//input[@name='name']")
            log.info(f"Finding job name field: {xpath_jobname}")
            jobname_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_jobname))
            )
            jobname_field.send_keys(job_name)
            time.sleep(4)

            # Click to upload file
            xpath_select_file = "//span[@class='cursor-pointer d-flex align-items-center upload-label']"
            log.info(f"Clicking file upload: {xpath_select_file}")
            select_file_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_select_file))
            )
            select_file_button.click()
            time.sleep(2)

            # Wait for the modal to appear
            modal_xpath = "//div[@class='modal-content popup']"
            log.info(f"Waiting for modal to appear: {modal_xpath}")
            modal_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, modal_xpath))
            )

            # Click on the drag and drop area
            xpath_drag_and_drop = ("//div[@class='modal-content popup']//div[@class='modal-body pl-4 "
                                   "cluster-create-main']//div[@class='file-uploader ']//div[@class='info-content']")
            log.info(f"Clicking drag and drop area: {xpath_drag_and_drop}")
            drag_and_drop_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_drag_and_drop))
            )
            drag_and_drop_element.click()

            time.sleep(2)

            # Find the file input element and send the file path
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(file_path)  # Send the file path obtained from JSON

            time.sleep(5)

            click_upload_button = self.driver.find_element(By.XPATH,
                                                           "//button[@class='btn btn-create ' and text()='Upload']")
            click_upload_button.click()
            time.sleep(5)

        except Exception as e:
            log.error(f"An error occurred: {str(e)}")
            raise  # Re-raise the exception after logging

        finally:
            # Clean up resources if needed
            pass
