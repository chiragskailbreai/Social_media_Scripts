from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import time
import os
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")
# Set up Chrome WebDriver (replace 'path_to_chromedriver' with your actual path)
driver = webdriver.Chrome(options=chrome_options)

# Open Instagram login page
driver.get('https://www.instagram.com/accounts/login/')
driver.maximize_window()
# Wait for the login page to load
time.sleep(5)

# Enter your Instagram credentials
username = 'kalibre20242024'
password = 'kalibre2024'

# Find the username and password fields and input the values
username_input = driver.find_element(By.NAME, 'username')
password_input = driver.find_element(By.NAME, 'password')
username_input.send_keys(username)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Wait for Instagram to log in (adjust the time if necessary)
time.sleep(10)

# Navigate to Instagram homepage after login
driver.get('https://www.instagram.com/')

# Wait for the page to load
time.sleep(5)


try:
    not_now_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Not Now']"))
    )
    not_now_button.click()  # Click the "Not Now" button
    print("Clicked 'Not Now' button.")
except Exception as e:
    print(f"'Not Now' button not found: {e}")



try:
    create_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd' and contains(., 'Create')]")))
    create_button.click()
except Exception as e:
    pass

    # Collect all child divs








# Wait for the upload dialog to open
time.sleep(3)

# File input element to upload the image (set the correct path to your image)
image_path = '/home/vithamas/Downloads/selenium.png'
file_input = driver.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')
file_input.send_keys(os.path.abspath(image_path))

# Wait for the image to be uploaded
time.sleep(5)

# Click 'Next' button after the image has been uploaded
next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Next')]"))
)
next_button.click()

# Wait for the next step to load
time.sleep(3)

next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Next')]"))
)
next_button.click()

# Find the caption text area and input the caption
try:
    caption_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a caption...']"))
    )
    caption_div.click()
    link ="https://www.google.co.in/"
    message = f"Your caption is ready with the\n {link}"
    # Example of using Unicode escape sequences for emojis
    caption_div.send_keys(message)  # 🎉😊🌟🚀

except Exception as e:
    print(f"Caption area not found: {e}")

# Wait for caption to be entered
time.sleep(3)

# Click 'Share' to post the image
share_button = driver.find_element(By.XPATH, '//div[contains(text(), "Share")]')
share_button.click()

# Wait a few seconds to make sure the post is uploaded
time.sleep(5)

# Close the browser
driver.quit()
