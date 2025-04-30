import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------
# CONFIGURATION AND ENVIRONMENT VALIDATION
# ---------------------------------------------

# Retrieve WiFi login credentials and SSID from environment variables
USER = os.getenv("Wifi_User_Id")
PASS = os.getenv("Wifi_Password")
SSID = os.getenv("SSID")

# Check that all required environment variables are set
if not USER or not PASS or not SSID:
    raise ValueError("🚨 [ERROR] One or more required environment variables (Wifi_User_Id, Wifi_Password, SSID) are not set.")

# Replace these placeholders with actual paths before running locally
brave_path = r"YOUR_BRAVE_BROWSER_PATH_HERE"
chromedriver_path = r"YOUR_CHROMEDRIVER_PATH_HERE"
LOGIN_URL = "http://122.252.242.93/"

# ---------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------

def check_aus_server():
    """Check if the AUS captive portal server is responding."""
    try:
        response = requests.get(LOGIN_URL, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def check_connection():
    """Check if the system is connected to any WiFi network."""
    print("🔍 [INFO] Checking WiFi connection...")
    output = os.popen("netsh wlan show interfaces").read()
    return "SSID" in output

def connect_to_wifi(ssid):
    """Connect to a predefined WiFi profile by SSID."""
    print(f"📶 [INFO] Connecting to {ssid}...")
    profiles = os.popen("netsh wlan show profiles").read()
    
    if ssid not in profiles:
        print(f"❌ [ERROR] Network profile '{ssid}' not found. Please configure it first.")
        return False

    os.system(f'netsh wlan connect name="{ssid}"')
    time.sleep(5)  # Give time for the connection to establish
    return True

def disconnect_from_network():
    """Disconnect from all WiFi networks."""
    print("🔌 [INFO] Disconnecting from WiFi...")
    os.system("netsh wlan disconnect")

def login_to_wifi():
    """Automate AUS WiFi login using Selenium with Brave browser."""
    print(f"🌐 [INFO] Opening login page: {LOGIN_URL}")

    # Set up Selenium with Brave
    options = Options()
    options.binary_location = brave_path  # Must be set to local Brave binary path
    options.add_argument("--start-maximized")

    try:
        service = Service(chromedriver_path)  # Must be set to local chromedriver executable path
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        raise RuntimeError(f"❌ [ERROR] WebDriver could not be started: {e}")

    try:
        driver.get(LOGIN_URL)
        print("✅ [SUCCESS] Login page loaded.")
    except Exception as e:
        driver.quit()
        raise ConnectionError(f"❌ [ERROR] Unable to open login page: {e}")

    try:
        # Wait until body is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Click "Campus User Login"
        print("➡️ [INFO] Navigating to Campus User Login page...")
        user_login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Campus User Login')]"))
        )
        user_login_btn.click()

        # Click "Existing User Login"
        print("➡️ [INFO] Navigating to Existing User Login page...")
        existing_login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Existing User Login')]"))
        )
        existing_login_btn.click()

        # Fill in credentials
        print("🔑 [INFO] Entering login credentials...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USER)
        driver.find_element(By.NAME, "password").send_keys(PASS)

        # Submit the form
        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Continue']").click()
        print("✅ [SUCCESS] Login submitted.")

        # Allow time for processing
        time.sleep(2)
    except Exception as e:
        raise RuntimeError(f"❌ [ERROR] Login automation failed: {e}")
    finally:
        driver.quit()

# ---------------------------------------------
# MAIN EXECUTION LOGIC
# ---------------------------------------------

if __name__ == "__main__":
    try:
        if not check_connection():
            if check_aus_server():
                disconnect_from_network()
                if connect_to_wifi(SSID):
                    login_to_wifi()
                else:
                    print("❌ [ERROR] Failed to connect to the specified WiFi network.")
            else:
                print("⚠️ [WARNING] AUS login server is unreachable. Check network or try later.")
        else:
            login_to_wifi()
    except Exception as err:
        print(f"🔥 [FATAL] An unexpected error occurred: {err}")
