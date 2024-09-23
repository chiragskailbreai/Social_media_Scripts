from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import os
from selenium.webdriver.common.action_chains import ActionChains
import emoji

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")  # This will store the profile
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def login_to_linkedin(driver, phone_number, password):
    driver.get("https://www.linkedin.com/login")
    
    # Check if we're already logged in
    if "feed" in driver.current_url:
        print("Already logged in!")
        return

    # Enter phone number
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    phone_input.send_keys(phone_number)
    
    # Enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    
    # Click login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "global-nav"))
    )

def post_to_linkedin(driver, text, image_path=None):
    # Navigate to LinkedIn homepage
    driver.get("https://www.linkedin.com/feed/")
    driver.maximize_window()
    # Click on "Start a post" button
    media = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Media']"))
    )
    media.click()
    
    # Wait for the post dialog to appear and switch to it

    
    if image_path:
        # Click on add image button
        # add_image_button = driver.find_element(By.XPATH, "//button[@aria-label='Add a photo']")
        # add_image_button.click()
        
        # Wait for file input to be present
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Send the image path to the input element (upload the image)
        file_input.send_keys(image_path)
        # ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        # Wait for image to upload
    # WebDriverWait(driver, 30).until(
    #     EC.invisibility_of_element_located((By.CSS_SELECTOR, ".share-box-file-viewer__file-name"))
    # )
    next_button = driver.find_element(By.XPATH,"//button[@aria-label='Next']")
    next_button.click()

    caption = driver.find_element(By.XPATH,"//div[@role='textbox']")
    caption.send_keys(text)
    time.sleep(5)

    elements = driver.find_elements(By.CLASS_NAME, 'basic-typeahead__selectable')

    # Access the element by index (e.g., index 0 for the first one)
    if elements:
        desired_element = elements[0]  # Change the index as needed
        # print(desired_element.text)
        desired_element.click()
    
    caption.send_keys(Keys.ENTER)
    caption_hastags = driver.find_element(By.XPATH,"//div[@role='textbox']")
    caption_hastags.send_keys(hashtag)

    
    # Click post button
    post_button = driver.find_element(By.XPATH, "//span[text()='Post']")
    post_button.click()
    
    # Wait for post to be published
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
    )

# def post_to_linkedin(driver, text, image_path=None):
#     # Navigate to LinkedIn homepage
#     driver.get("https://www.linkedin.com/feed/")
    
#     # Click on "Start a post" button
#     post_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[text()='Start a post']"))
#     )
#     post_button.click()
    
#     # Wait for the post dialog to appear
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
#     )

#     # If an image is provided, directly send the image path to the hidden file input
#     if image_path:
#         # Find the hidden file input for adding media (photo)
#         file_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
#         )
        
#         # Send the image path to the input element (upload the image)
#         file_input.send_keys(image_path)
        
#         # Wait for the image to upload
#         WebDriverWait(driver, 30).until(
#             EC.invisibility_of_element_located((By.CSS_SELECTOR, ".share-box-file-viewer__file-name"))
#         )
    
#     # Enter the post caption
#     caption_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
#     caption_box.send_keys(text)
    
#     # Click the "Post" button to publish the post
#     publish_button = driver.find_element(By.XPATH, "//span[text()='Post']")
#     publish_button.click()
    
#     # Wait for the post to be published
#     WebDriverWait(driver, 10).until(
#         EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
#     )


# Main execution
if __name__ == "__main__":
    # Replace with your LinkedIn credentials
    PHONE_NUMBER = "9483225221"
    PASSWORD = "kalibre2024"
    
    # Your post content
    link="https://www.google.co.in/"
    company = "kalibre"
    POST_TEXT = f"\nHello LinkedIn!.\n{link}  \n @{company}" 
    hashtag = f"\n#kalibre #Jobs #Freshers"
    IMAGE_PATH = r"/home/vithamas/Downloads/selenium.png"  # Optional: replace with the path to your image
    
    # Set up the WebDriver
    driver = setup_driver()
    
    try:
        login_to_linkedin(driver, PHONE_NUMBER, PASSWORD)
        post_to_linkedin(driver, POST_TEXT, IMAGE_PATH)
        print("Successfully posted to LinkedIn")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the browser
        driver.quit()