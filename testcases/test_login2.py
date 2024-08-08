import time
import json
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from pages.loginpage import LoginPage
from pages.AlphafoldPipeline import AlphafoldPipeline
from pages.CreateWorkspace import CreateWorkspace
from pages.DeleteWorkspace import DeleteWorkspace
from pages.StopWorkspace import StopWorkspace
from pages.RestartWorkspace import RestartWorkspace
from pages.StartWorkspace import StartWorkspace
from pages.SharingWorkspace import SharingWorkspace
from testcases.dev_BaseClass import dev_BaseClass


@pytest.mark.usefixtures("driver_setup")
class TestWorkspace(dev_BaseClass):
    driver: webdriver.Chrome

    def test_login(self):
        log = self.getLogger()
        log.info("Starting login test.")
        lp = LoginPage(self.driver)
        lp.module()
        log.info("Login test completed.")

    '''   

    @pytest.mark.parametrize("workspace_data", json.load(
        open("/Users/nishantchauhan/PycharmProjects/QuarkAutomation/testcases/workspace_data.json"))["workspaces"])
    def test_create_workspace(self, workspace_data):
        #log.info("Clicking pipeline tab.")
        workspace_tab = self.driver.find_element(By.XPATH, dev_BaseClass.Workspace_ICON)
        workspace_tab.click()
        log = self.getLogger()
        log.info(f"Creating workspace with data: {workspace_data}")
        cw = CreateWorkspace(self.driver)
        cw.create(workspace_data)
    '''

    def test_click_pipeline_tab_and_launchpad(self):
        log = self.getLogger()
        log.info("Clicking pipeline tab.")
        pipeline_tab = self.driver.find_element(By.XPATH, dev_BaseClass.Pipeline_tab)
        pipeline_tab.click()
        time.sleep(4)
        log.info("Clicking launchpad tab.")
        launchpad_tab = self.driver.find_element(By.XPATH, dev_BaseClass.Launchpad_tab)
        launchpad_tab.click()
        time.sleep(5)

    @pytest.mark.parametrize("pipeline_data", json.load(open("/Users/nishantchauhan/PycharmProjects/QuarkAutomation"
                                                             "/testcases/pipelines.json"))["pipelines"])
    def test_create_pipeline(self, pipeline_data):
        log = self.getLogger()
        log.info(f"Creating pipeline with config: {pipeline_data}")
        test1 = AlphafoldPipeline(self.driver)
        test1.create_pipeline(pipeline_data)

    def test_connect_workspace(self):
        log = self.getLogger()
        log.info("Connecting to workspace.")
        obj3 = DeleteWorkspace(self.driver)
        obj3.delete_workspace()

    def test_stop_workspace(self):
        log = self.getLogger()
        log.info("Stopping workspace.")
        self.driver.find_element(By.XPATH, "//span[@class='menu-name'][normalize-space()='Workspaces']").click()
        time.sleep(5)
        obj1 = StopWorkspace(self.driver)
        obj1.stop_workspaces()

    def test_start_workspace(self):
        log = self.getLogger()
        log.info("Starting workspace.")
        refresh_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'refreshingIcon')]")
        refresh_button.click()
        time.sleep(5)
        obj = StartWorkspace(self.driver)
        obj.process_workspaces()

    def test_restart_workspace(self):
        log = self.getLogger()
        log.info("Restarting workspace.")
        refresh_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'refreshingIcon')]")
        refresh_button.click()
        time.sleep(5)
        obj2 = RestartWorkspace(self.driver)
        obj2.restart_workspaces()

    def test_share_workspace(self):
        log = self.getLogger()
        log.info("Sharing workspace.")
        refresh_button = self.driver.find_element(By.XPATH, "//span[contains(@class, 'refreshingIcon')]")
        refresh_button.click()
        time.sleep(5)
        obj4 = SharingWorkspace(self.driver)
        obj4.sharing_workspaces()

    def test_delete_workspace(self):
        log = self.getLogger()
        log.info("Deleting workspace.")
        obj4 = DeleteWorkspace(self.driver)
        obj4.delete_workspace()
        delete_buttons = self.driver.find_elements(By.XPATH, "//span[@class='icon' and @data-tip='Delete']")

        if not delete_buttons:
            log.info("No workspaces left to delete.")
        else:
            log.info("There are still workspaces left to delete.")
