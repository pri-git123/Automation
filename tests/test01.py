import subprocess
import time
from select import select

from selenium.common import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

# Set the path to your private key file and SSH details
ssh_key_path = '/Users/nishantchauhan/Downloads/private-browser.pem'
ssh_host = 'ec2-user@34.199.223.179'
local_port = 3128

# Check if the port is already in use
try:
    subprocess.run(["lsof", "-i", f":{local_port}"], check=True)
    print(f"Port {local_port} is already in use. Exiting.")
    exit()
except subprocess.CalledProcessError:
    pass  # Port is not in use

# Construct the SSH command
ssh_command = f"ssh -ND {local_port} -v -i {ssh_key_path} {ssh_host}"

ssh_process = subprocess.Popen(ssh_command, shell=True)
time.sleep(30)

# Configure Firefox profile with SOCKS5 proxy
profile = webdriver.FirefoxProfile()
print("Proxy settings in Firefox profile:")
for key, value in profile.DEFAULT_PREFERENCES.items():
    print(f"{key}: {value}")

proxy = ('127.0.0.1', 3128)  # Local SOCKS proxy

options = Options()
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', proxy[0])
options.set_preference('network.proxy.socks_port', proxy[1])
options.set_preference('network.proxy.socks_remote_dns', True)
options.add_argument('--proxy-server=socks://127.0.0.1:3128')
options.set_preference('network.proxy.socks_remote_dns', True)

options.headless = False
driver = webdriver.Firefox(options=options)

driver.maximize_window()
time.sleep(5)
driver.get("https://regn.invisibl.io/")
science_cloud_module = driver.find_element(By.XPATH,
                                           "//a[@class='grid-item' and @href='/app/']/label[text()='Science Cloud']")
science_cloud_module.click()
main_window_handle = driver.current_window_handle
# Wait for the new window to open
new_window_handle = WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

# Switch to the new window
all_window_handles = driver.window_handles
new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
driver.switch_to.window(new_window_handle)

####credentials
email_xpath = "//form[@method='post']//input[@id='login']"
password_xpath = "//form[@method='post']//input[@id='password']"

element_email = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, email_xpath))
)
element_email.send_keys("raghuraman.balachand@regeneron.com")

element_password = driver.find_element(By.XPATH, password_xpath)
element_password.send_keys("jh2348fijk34b59sdf4kj")
time.sleep(5)
driver.find_element(By.ID, 'submit-login').click()

time.sleep(20)
# Continue with the rest of your script...
driver.find_element(By.XPATH, "//a[contains(@class, 'btn-create') and contains(., 'Add New')]").click()
# driver.find_element(By.XPATH,"//div[text()='Basic JupyterLab with GPU']]").click()

####Basic JupyterLab
time.sleep(10)
driver.find_element(By.XPATH, '//div[text()="Basic JupyterLab"]').click()
# driver.find_element(By.XPATH,"//button[@class='edit-button edit-labeled float-right bg-transparent' and @type='button']").click()
time.sleep(10)
driver.find_element(By.XPATH, "//form[@class='workspace-box-full-height']//input[@name='name']").send_keys(
    "ws-basicjupyter")

forms = driver.find_elements(By.XPATH, "//form[@class='workspace-box-full-height']")

last_form = forms[-1]
driver.execute_script("arguments[0].scrollIntoView();", last_form)

# Find and click the Edit button
edit_button_xpath = "//form[@class='workspace-box-full-height']//button[@class='edit-button edit-labeled float-right bg-transparent']/div[@class='right-edit']"
edit_button = driver.find_element(By.XPATH, edit_button_xpath)
edit_button.click()
#####cpu inputs
# input_element_xpath = "//div[@class='col-6']//input[@class='form-control' and @type='number' and @name='capacity.resources.cpu.value']"
input_cpu_xpath = "//div//input[@type='number' and @name='capacity.resources.cpu.value']"
input_cpu = driver.find_element(By.XPATH, input_cpu_xpath)
input_cpu.clear()
input_cpu.send_keys('252')
### values for memeory
input_memory_xpath = "//div//input[@type='number' and @name='capacity.resources.memory.value']"
input_memory = driver.find_element(By.XPATH, input_memory_xpath)
input_memory.clear()
input_memory.send_keys('250')
driver.find_element(By.XPATH, "//select[@name='capacity.resources.cpu.unit']/option[@value='m']")
# Clear the existing value
# Enter a new value (replace 'new_value' with the desired value)
dropdown_cpu = Select(driver.find_element(By.NAME, "capacity.resources.cpu.unit"))
dropdown_cpu.select_by_value('m')
dropdown_memory = Select(driver.find_element(By.NAME, "capacity.resources.memory.unit"))
dropdown_memory.select_by_value("Mi")
driver.find_element(By.XPATH, "//button[contains(@class, 'edit-button') and contains(@class, 'edit-labeled')]").click()
########click on launch
driver.find_element(By.XPATH, "//button[contains(@class, 'btn-create') and contains(@type,'submit') ]").click()

delete_buttons = driver.find_elements(By.XPATH, "//span[@data-tip='Delete']/span[@class='icon-delete black']")
# Iterate through each delete button and click it

for delete_button in delete_buttons:
    delete_button.click()
    # alert = Alert(driver)

    wait = WebDriverWait(driver, 20)
    modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'react-confirm-alert')))
    print(modal)
    # Locate the input field in the modal
    workspace_name_input = modal.find_element(By.ID, 'version-update')

    # Enter the workspace name into the input field
    workspace_name_input.clear()  # Clear any existing value
    workspace_name_input.send_keys("test01")

    # Locate and click the "Delete" button
    delete_button_modal = modal.find_element(By.XPATH, "//button[contains(text(), 'Delete')]")
    delete_button_modal.click()

    # Optionally, wait for some time to ensure the workspace is deleted successfully
    driver.implicitly_wait(3)

#####
# delete_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@data-tip='Delete']/span[@class='icon-delete black']")))


# for delete_button in delete_buttons:
try:
    # Wait for the element to be present in the DOM
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[@class="icon-delete black"]'))
    )
    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element.click()
    time.sleep(4)
    # cancel_text=driver.find_element(By.XPATH,"//button[@class='btn btn-default' and text()='Cancel']")
    # cancel_text.click()
    # print("--------------------", cancel_text.text)
    input_box = driver.find_element(By.XPATH, "//input[@type='text' and @id='version-update']")
    input_box.send_keys("test-demo10")
    print("-----------------", input_box)
    driver.find_element(By.XPATH, "//button[@type='submit' and @class='btn btn-create']").click()


except Exception as e:
    # Handle the exception or raise it again if needed
    raise e

except NoAlertPresentException:
    print("No alert present")
# Switching to the alert

ssh_process.terminate()
