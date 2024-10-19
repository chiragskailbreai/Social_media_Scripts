import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import urllib.parse

def setup_driver():
    chrome_options = Options()
    user_data_dir = "/home/vithamas/.config/google-chrome/Profile 7"  # Update this path
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def read_groups_from_csv(file_path):
    groups = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header row
        for row in csv_reader:
            if row:
                # Extract group name, removing numbering and extra information
                group_info = row[0].split(') ', 1)[-1].split(' with ', 1)[0].strip()
                group_name = group_info.strip('"')  # Remove surrounding quotes if present
                groups.append(group_name)
    return groups

def search_group(driver, group_name):
    try:
        search_url = f"https://www.linkedin.com/search/results/groups/?keywords={urllib.parse.quote(group_name)}"
        driver.get(search_url)
        
        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-result__info"))
        )
        
        # Check if the group is found
        group_elements = driver.find_elements(By.CSS_SELECTOR, ".search-result__info")
        for element in group_elements:
            title_element = element.find_element(By.CSS_SELECTOR, ".search-result__title")
            if group_name.lower() in title_element.text.lower():
                print(f"Found group: {group_name}")
                return True
        
        print(f"Group not found: {group_name}")
        return False
    
    except Exception as e:
        print(f"Error searching for group '{group_name}': {str(e)}")
        return False

def linkedin_group_searcher(csv_file_path):
    driver = setup_driver()
    groups = read_groups_from_csv(csv_file_path)

    try:
        # Login to LinkedIn (assuming you're already logged in due to the user profile)
        driver.get("https://www.linkedin.com")
        time.sleep(5)  # Wait for page to load

        for group in groups:
            search_group(driver, group)
            time.sleep(2)  # Short pause between searches

    finally:
        driver.quit()

if __name__ == "__main__":
    csv_file_path = "linkedin_groups.csv"  # Update this with the actual path to your CSV file
    linkedin_group_searcher(csv_file_path)