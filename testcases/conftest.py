import time

import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from testcases.dev_BaseClass import dev_BaseClass


@pytest.fixture(scope="class")
def driver_setup(request):
    log = dev_BaseClass.getLogger()
    log.info("Setting up the driver")

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    driver.get("https://dev2.gravity.invisibl.io/")
    time.sleep(10)
    driver.maximize_window()
    yield
    driver.close()

