# webdriver_setup.py

import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def setup_proxy_and_driver(ssh_key_path, ssh_host, local_port):
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

    proxy = ('127.0.0.1', local_port)  # Local SOCKS proxy

    options = Options()
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', proxy[0])
    options.set_preference('network.proxy.socks_port', proxy[1])
    options.set_preference('network.proxy.socks_remote_dns', True)
    options.add_argument('--proxy-server=socks://127.0.0.1:3128')
    options.set_preference('network.proxy.socks_remote_dns', True)

    options.headless = False
    driver = webdriver.Firefox(options=options)
    driver.get("https://stg1.quark.invisibl.io/")
    driver.maximize_window()

    return driver, ssh_process
