import time

import pytest
import json

from selenium.webdriver.common.by import By

from pages.ConnectWorkspace import ConnectWorkspace
from pages.CreateWorkspace import CreateWorkspace
from pages.DeleteWorkspace import DeleteWorkspace
from pages.RestartWorkspace import RestartWorkspace
from pages.SharingWorkspace import SharingWorkspace
from pages.StartWorkspace import StartWorkspace
from pages.StopWorkspace import StopWorkspace
from pages.loginpage import LoginPage
from pages.RefreshPage import RefreshPage
from testcases.dev_BaseClass import dev_BaseClass
from testcases.proxy_setup import setup_proxy_and_driver


@pytest.fixture(scope="function")
def driver_and_proxy():
    ssh_key_path = '/Users/nishantchauhan/Downloads/private-browser.pem'
    ssh_host = 'ec2-user@34.199.223.179'
    local_port = 3128
    driver, ssh_process = setup_proxy_and_driver(ssh_key_path, ssh_host, local_port)
    yield driver
    driver.quit()
    ssh_process.terminate()


@pytest.fixture(scope="function")
def logged_in_driver(driver_and_proxy):
    driver = driver_and_proxy
    login_page = LoginPage(driver)
    login_page.module()
    yield driver


class TestWorkspace(dev_BaseClass):
    def test_login(self, logged_in_driver):
        try:
            # Test login functionality
            pass
        except Exception as e:
            print("An error occurred during login:", e)
            pytest.fail("Test failed due to login error")

    def test_refresh(self, logged_in_driver):
        try:
            # Test refresh functionality
            restart = RefreshPage(logged_in_driver)
            restart.click_second_option()
        except Exception as e:
            print("An error occurred during refresh:", e)
            pytest.fail("Test failed due to refresh error")

    @pytest.mark.parametrize("workspace_data", json.load(
        open("/Users/nishantchauhan/PycharmProjects/InvisblProject/testcases/workspace_data.json"))["workspaces"])
    def test_createworkspace(self, logged_in_driver, workspace_data):
        try:
            # Test create workspace functionality
            cw = CreateWorkspace(logged_in_driver)
            cw.create(workspace_data)
        except Exception as e:
            print("An error occurred during workspace creation:", e)
            pytest.fail("Test failed due to workspace creation error")

    def test_restart(self, logged_in_driver):
        try:
            # Test restart workspace functionality
            restartable = RestartWorkspace(logged_in_driver)
            restartable.restart_workspaces()
        except Exception as e:
            print("An error occurred during workspace restart:", e)
            pytest.fail("Test failed due to workspace restart error")

    def test_connectworkspace(self, logged_in_driver):
        try:
            # Test connect workspace functionality
            obj3 = ConnectWorkspace(logged_in_driver)
            obj3.connect_demoprotein()
        except Exception as e:
            print("An error occurred during workspace connection:", e)
            pytest.fail("Test failed due to workspace connection error")

    def test_Shareworkspace(self, logged_in_driver):
        try:
            # Test share workspace functionality
            obj4 = SharingWorkspace(logged_in_driver)
            obj4.sharing_workspaces()
        except Exception as e:
            print("An error occurred during workspace sharing:", e)
            pytest.fail("Test failed due to workspace sharing error")

    def test_stopworkspace(self, logged_in_driver):
        try:
            # Test stop workspace functionality
            obj4 = StopWorkspace(logged_in_driver)
            obj4.stop_workspaces()
        except Exception as e:
            print("An error occurred during workspace stop:", e)
            pytest.fail("Test failed due to workspace stop error")

    def test_startworkspace(self, logged_in_driver):
        try:
            # Test start workspace functionality
            obj4 = StartWorkspace(logged_in_driver)
            obj4.process_workspaces()
        except Exception as e:
            print("An error occurred during workspace start:", e)
            pytest.fail("Test failed due to workspace start error")

    def test_deleteworkspace(self, logged_in_driver):
        try:
            log = self.getLogger()
            log.info("Starting the test_deleteworkspace method.")

            # Test delete workspace functionality
            delete = DeleteWorkspace(logged_in_driver)
            delete.delete_workspace()

            # Check if any workspaces remain after attempting deletion
            remaining_workspaces = logged_in_driver.find_elements(By.XPATH, "//span[@class='icon' and "
                                                                            "@data-tip='Delete']")
            assert len(remaining_workspaces) == 0, "Some workspaces were not deleted successfully."

            log.info("All workspaces were deleted successfully.")
            log.info("Finished the test delete workspace method.")
        except Exception as e:
            print("An error occurred during workspace deletion:", e)
            pytest.fail("Test failed due to workspace deletion error")
