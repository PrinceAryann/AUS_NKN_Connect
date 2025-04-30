---
# **WiFi Login Automation Script**

This Python script automates the process of logging into a WiFi network with captive portal authentication. It uses Selenium and the Brave browser to interact with the login page.
---

## **Prerequisites**

1. **Python**: Ensure you have Python 3.x installed on your machine.

   - Install Python from [python.org](https://www.python.org/).

2. **Install Dependencies**: The script requires several Python libraries to run.

   - Install them using `pip`:

   ```bash
   pip install selenium requests
   ```

3. **Brave Browser**:

   - Download and install the Brave browser from [brave.com](https://brave.com/).
   - Once installed, provide the path to the Brave browser binary in the `brave_path` variable.

4. **Chromedriver**:
   - Download the appropriate version of [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) that matches your browser version.
   - Extract the `chromedriver.exe` file and provide its path in the `chromedriver_path` variable.

---

## **Environment Variables**

To run the script successfully, set the following environment variables:

- **Wifi_User_Id**: Your WiFi login username.
- **Wifi_Password**: Your WiFi login password.
- **SSID**: The SSID (WiFi name) you want to connect to.

You can set these environment variables in your terminal (for Linux/macOS):

```bash
export Wifi_User_Id="your_user_id"
export Wifi_Password="your_password"
export SSID="your_wifi_ssid"
```

Or for Windows:

```bash
set Wifi_User_Id="your_user_id"
set Wifi_Password="your_password"
set SSID="your_wifi_ssid"
```

Alternatively, you can hardcode these values into the script (not recommended for production).

---

## **Setup Instructions**

### 1. **Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/wifi-login-automation.git
cd wifi-login-automation
```

### 2. **Update Paths in the Script**

In the `wifi_login.py` script, replace the following placeholders with the actual paths for your Brave browser and Chromedriver:

```python
brave_path = r"YOUR_BRAVE_BROWSER_PATH_HERE"
chromedriver_path = r"YOUR_CHROMEDRIVER_PATH_HERE"
```

For example, on Windows, the paths could be:

```python
brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
chromedriver_path = r"D:/path/to/chromedriver.exe"
```

### 3. **Run the Script**

Once everything is set up, you can run the script using the following command:

```bash
python wifi_login.py
```

The script will:

1. Check if you are connected to the WiFi.
2. If not connected, it will attempt to connect to the specified WiFi (SSID).
3. It will then automate the login process using Selenium and the Brave browser.

---

## **Additional Notes**

1. **Captive Portal Detection**: The script assumes that the captive portal login page appears automatically when connecting to the WiFi. If it doesn't, you may need to manually disable the captive portal detection feature on your system. This can be done via the Windows registry:

   - To disable:

     ```bash
     reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet" /v EnableActiveProbing /t REG_DWORD /d 0 /f
     ```

   - To enable:
     ```bash
     reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet" /v EnableActiveProbing /t REG_DWORD /d 1 /f
     ```

2. **Running as Administrator**: Some commands in the script (like connecting to WiFi) may require administrative privileges. Make sure to run the script with administrator rights.

3. **Troubleshooting**: If you encounter errors, make sure that:
   - The `chromedriver.exe` and Brave browser paths are correct.
   - The required Python libraries are installed.
   - Your environment variables are set correctly.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
