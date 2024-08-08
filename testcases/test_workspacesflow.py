import time
import json
import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from pages.StartWorkspace import StartWorkspace
from pages.StopWorkspace import StopWorkspace
from pages.loginpage import LoginPage
from pages.CreateWorkspace import CreateWorkspace
from testcases.dev_BaseClass import dev_BaseClass
import logging


@pytest.mark.usefixtures("driver_setup")
class TestWorkspace(dev_BaseClass):
    driver: webdriver.Chrome

    def test_login(self):
        lp = LoginPage(self.driver)
        lp.module()

    @pytest.mark.parametrize("workspace_data", json.load(
        open("/testcases/workspace_data.json"))["workspaces"])
    def test_createworkspace(self, workspace_data):
        cw = CreateWorkspace(self.driver)
        cw.create(workspace_data)

    def test_startworkspace(self):
        lp = LoginPage(self.driver)
        lp.module()
        startobject = StartWorkspace(self.driver)
        startobject.start_workspaces()

    def test_stopworkspace(self):
        lp = LoginPage(self.driver)
        lp.module()
        stopobj=StopWorkspace(self.driver)
        stopobj.stop_workspaces()


