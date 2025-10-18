import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pyautogui 

DEBUG_PORT = 9222
USER_DATA_DIR = r"C:\temp\chrome_profile_x"  
WAIT_SECONDS = 5

def attach_selenium_to_debugger(port=9222):
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=options) 
    return driver
    
def main():
    # Load user credentials from data.json
    try:
        with open('data.json') as user_data:
            data = json.load(user_data)
    except FileNotFoundError:
        print("Error: 'data.json' not found.")
        return
    
    # Validate credentials 
    if data.get("USERNAME") == "***" or data.get("PASSWORD") == "***":
        print("Error: Set your USERNAME and PASSWORD in 'data.json'")
        return
    
    try:
        # Target URL for account deactivation
        url = "https://x.com/settings/deactivate"

        # Candidate paths for the Chrome executable
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            shutil.which("chrome"),
        ]

        # Pick the first valid Chrome executable found
        chrome = next(p for p in candidates if p and shutil.which(p))

        if not chrome:
            raise RuntimeError("Chrome browser not found.")

        # Launch Chrome with remote debugging enabled so Selenium can attach to it.
        subprocess.Popen([
            chrome,
            f"--remote-debugging-port={DEBUG_PORT}",
            f"--user-data-dir={USER_DATA_DIR}",
            "--incognito",
            url
        ], shell=False)

        # Use pyautogui to avoid login automation blocks
        time.sleep(8)
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.write(data["USERNAME"])
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write(data["PASSWORD"])
        pyautogui.press("enter")
        time.sleep(2)
        
        # Connect Selenium to browser
        driver = attach_selenium_to_debugger(port=DEBUG_PORT)
        driver.switch_to.window(driver.window_handles[-1])  
        wait = WebDriverWait(driver, WAIT_SECONDS)

        # Reactivate account if already deactivated
        try:
            if data.get("DEACTIVATE", False):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Yes, reactivate" or text()="Sí, reactivar" or text()="Sim, reativar"]'))).click()
        except:
            print("-Reactivation button not found. Continuing normally-")

        # Click "Deactivate" button
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Deactivate" or text()="Desactivar" or text()="Desativar"]'))).click()

        # Enter password to confirm deactivation
        password = wait.until(EC.presence_of_element_located((By.NAME, "current_password")))
        password.send_keys(data["PASSWORD"])

        # Click "Deactivate" button
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Deactivate" or text()="Desactivar" or text()="Desativar"]'))).click()

        # Verify deactivation by checking redirected URL
        try:
            wait.until(EC.url_contains("/settings/deactivated"))

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            next_month = datetime.now() + relativedelta(months=1, days=-1)
            formatted_date = next_month.strftime("%Y-%m-%d")

            with open("status.log", "w") as file:
                file.write(f"Account successfully deactivated!\nYou have until {formatted_date} to reactivate your account.\nYou can set a reminder or automate the launch of this script.")
            print("-Account deactivated successfully-")
        except Exception:
            with open("status.log", "w") as file:
                file.write("Error verifying account deactivation via URL change.")     
    except Exception as e:
        print("Error:", e)
    finally:
        pass

if __name__ == "__main__":
    main()
