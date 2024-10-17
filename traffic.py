import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException, NoSuchWindowException, WebDriverException
import pyautogui
from math import factorial

def Random_Keywords():
    keywords = [
        "Latest Active Frontend Developer jobs in MAANG+ ...",
        "Latest active jobs at Mature-stage startups",
        "Latest Active Automation Test Engineer jobs in AI/ML ...",
        "Latest Active Jobs at Top Tech Companies and High Growth Startups",
        "Latest Active jobs in Bengaluru",
        "Latest Active jobs in SaaS companies, India ",
        "Latest Active jobs in Cloud Computing companies",
        "Latest Active jobs in Mumbai, India"
    ]
    return random.choice(keywords)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    latitude, longitude = random.uniform(28.0, 30.0), random.uniform(76.0, 78.0)
    chrome_options.add_argument(f"--geolocation={latitude},{longitude}")
    
    languages = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-IN,en;q=0.7"]
    chrome_options.add_argument(f"--lang={random.choice(languages)}")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def safe_execute(driver, action):
    try:
        return action()
    except NoSuchWindowException:
        print("Window was closed unexpectedly. Attempting to switch to main window.")
        driver.switch_to.window(driver.window_handles[0])
    except WebDriverException as e:
        print(f"WebDriver error occurred: {str(e)}")
    return None

def simulate_realistic_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.3))
        
        if random.random() < 0.05:
            typo = random.choice('abcdefghijklmnopqrstuvwxyz')
            element.send_keys(typo)
            time.sleep(random.uniform(0.2, 0.5))
            element.send_keys(Keys.BACKSPACE)
            time.sleep(random.uniform(0.2, 0.5))
            element.send_keys(char)

def simulate_realistic_scrolling(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    
    current_position = 0
    while current_position < total_height:
        scroll_amount = random.randint(int(viewport_height * 0.3), int(viewport_height * 0.7))
        current_position += scroll_amount
        
        start_time = time.time()
        duration = random.uniform(0.5, 1.5)
        while time.time() - start_time < duration:
            y = int(easeInOutQuad(time.time() - start_time, 0, scroll_amount, duration))
            driver.execute_script(f"window.scrollTo(0, {current_position - scroll_amount + y});")
            time.sleep(0.01)
        
        time.sleep(random.uniform(1, 3))
        
        if random.random() < 0.2:
            up_amount = random.randint(int(viewport_height * 0.1), int(viewport_height * 0.3))
            current_position -= up_amount
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(random.uniform(0.5, 1.5))

def easeInOutQuad(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t + b
    t -= 1
    return -c/2 * (t*(t-2) - 1) + b

def simulate_mouse_movement():
    screen_width, screen_height = pyautogui.size()
    start_x, start_y = pyautogui.position()
    end_x = random.randint(0, screen_width)
    end_y = random.randint(0, screen_height)
    
    control_points = [
        (start_x, start_y),
        (random.randint(0, screen_width), random.randint(0, screen_height)),
        (random.randint(0, screen_width), random.randint(0, screen_height)),
        (end_x, end_y)
    ]
    
    steps = 50
    for i in range(steps + 1):
        t = i / steps
        x = int(bezier(t, [p[0] for p in control_points]))
        y = int(bezier(t, [p[1] for p in control_points]))
        pyautogui.moveTo(x, y)
        time.sleep(random.uniform(0.01, 0.03))

def bezier(t, points):
    n = len(points) - 1
    return sum(comb(n, i) * (1-t)**(n-i) * t**i * points[i] for i in range(n+1))

def comb(n, k):
    return factorial(n) // (factorial(k) * factorial(n-k))

def search_on_google(driver, query):
    driver.get("https://www.google.com/")
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
    
    simulate_realistic_typing(search_box, query)
    
    time.sleep(random.uniform(0.5, 1.5))
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

def perform_random_actions(driver, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        action = random.choice([simulate_realistic_scrolling, click_random_element, simulate_mouse_movement])
        safe_execute(driver, lambda: action(driver) if action != simulate_mouse_movement else action())
        time.sleep(random.uniform(0.5, 1.5))

def click_random_element(driver):
    clickable_elements = ['a', 'button', 'input[type="submit"]', 'input[type="button"]']
    selector = random.choice(clickable_elements)
    
    try:
        elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        
        visible_elements = [elem for elem in elements if safe_execute(driver, elem.is_displayed) and safe_execute(driver, elem.is_enabled)]
        
        if visible_elements:
            element = random.choice(visible_elements)
            safe_execute(driver, lambda: driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element))
            time.sleep(random.uniform(0.5, 1.0))
            
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, element.get_attribute('xpath'))))
            
            safe_execute(driver, element.click)
            time.sleep(random.uniform(1, 2))
            safe_execute(driver, driver.back)
    except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException):
        print("Failed to click a random element.")
    except Exception as e:
        print(f"An unexpected error occurred while clicking: {str(e)}")

def kalibre_logo_click(driver):
    logo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@alt="Kalibre logo"]')))
    time.sleep(2)
    actions = ActionChains(driver)
    actions.move_to_element(logo).click().perform()
    time.sleep(4)

def Kalibre_button(driver):
    wait = WebDriverWait(driver, 10)
    button_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MuiStack-root.mui-ykhfo7")))
    buttons = button_container.find_elements(By.TAG_NAME, "button")
    if len(buttons) >= 4:
        location_button = buttons[3]
        location_button.click()
        time.sleep(3)

    try:
        target_div = None
        scroll_attempts = 0
        max_scroll_attempts = 20

        while not target_div and scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(0.5)
            try:
                target_div = driver.find_element(By.CLASS_NAME, "MuiStack-root.mui-19je7t9")
            except:
                scroll_attempts += 1

        if target_div:
            first_inner_div = target_div.find_element(By.TAG_NAME, "div")
            time.sleep(3)
            first_inner_div.click()
            driver.execute_script("window.open(arguments[0].href);", first_inner_div)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(4)
            driver.close()
            driver.switch_to.window(driver.window_handles[-2])
        else:
            print("Target div not found on Kalibre website after scrolling.")
    except Exception as e:
        print(f"An error occurred during Kalibre-specific actions: {str(e)}")

def Kalibre_Random_Apply_button(driver):
    try:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "MuiButton-root") and contains(text(), "Apply")]')))
        if button.is_displayed():
            actions = ActionChains(driver)
            actions.move_to_element(button).context_click().perform()
            actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[-1])
            simulate_realistic_scrolling(driver)
            time.sleep(3)
            driver.close()
            driver.switch_to.window(driver.window_handles[-2])
    except Exception as e:
        print(f"Error in Kalibre_Random_Apply_button: {str(e)}")

def Kalibre_Filter_Buttons(driver):
    try:
        parent_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'MuiCardContent-root.mui-1822eo3')))
        span_elements = parent_div.find_elements(By.XPATH, './/div[contains(@class, "MuiBox-root mui-odz94x")]//span[contains(@class, "MuiTypography-root MuiTypography-body1")]')
        if span_elements:
            random_span = random.choice(span_elements)
            random_span.click()
            print(f'Clicked on: {random_span.text}')
        else:
            print("No span elements found.")
        time.sleep(2)
    except Exception as e:
        print(f"Error in Kalibre_Filter_Buttons: {str(e)}")

def kalibre_Actions(driver):
    actions = [
        Kalibre_button,
        Kalibre_Filter_Buttons,
        Kalibre_Random_Apply_button,
    ]
    random.choice(actions)(driver)

def visit_websites(driver, kalibre_index, results):
    other_indices = [i for i in range(len(results)) if i != kalibre_index]
    
    num_other_sites = random.randint(2, 3)
    other_sites_to_visit = random.sample(other_indices, min(num_other_sites, len(other_indices)))
    
    sites_to_visit = other_sites_to_visit + [kalibre_index]
    random.shuffle(sites_to_visit)

    for idx in sites_to_visit:
        try:
            result = results[idx]
            safe_execute(driver, lambda: result.send_keys(Keys.CONTROL + Keys.RETURN))
            time.sleep(random.uniform(2, 4))
            
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                simulate_mouse_movement()
            else:
                print("Failed to open new tab. Continuing with the current page.")
            
            safe_execute(driver, lambda: ActionChains(driver).send_keys(Keys.ESCAPE).perform())
            time.sleep(random.uniform(1, 2))
            
            if idx == kalibre_index:
                kalibre_logo_click(driver)
                num_actions = random.randint(2, 4)
                for _ in range(num_actions):
                    kalibre_Actions(driver)
                    time.sleep(random.uniform(2, 4))
            else:
                perform_random_actions(driver, random.uniform(5, 10))
            
            time.sleep(random.uniform(1, 2))
            safe_execute(driver, driver.close)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"An error occurred while visiting a website: {str(e)}")
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[0])

def go_to_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'pnnext'))
        )
        safe_execute(driver, next_button.click)
        time.sleep(random.uniform(2, 4))
        return True
    except (TimeoutException, NoSuchElementException):
        print("No more pages to search.")
        return False

def search_until_kalibre_found(driver, keyword):
    kalibre_found = False
    page_count = 0
    max_pages = 5
    
    while not kalibre_found and page_count < max_pages:
        try:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf a'))
            )
            
            kalibre_index = -1
            for index, result in enumerate(results):
                link = safe_execute(driver, lambda: result.get_attribute('href'))
                if link and "kalibre.ai" in link:
                    kalibre_index = index
                    kalibre_found = True
                    break
            
            if kalibre_found:
                visit_websites(driver, kalibre_index, results)
            else:
                print(f"Kalibre not found on page {page_count + 1}. Moving to next page...")
                if not go_to_next_page(driver):
                    break
            
            page_count += 1
        except Exception as e:
            print(f"An error occurred while searching: {str(e)}")
            break
    
    if not kalibre_found:
        print(f"Kalibre not found after searching {page_count} pages.")

def main():
    driver = setup_driver()
    
    try:
        for i in range(random.randint(2, 4)):  # Random number of search iterations
            keyword = Random_Keywords()
            print(f"Searching for: {keyword}")
            search_on_google(driver, keyword)
            search_until_kalibre_found(driver, keyword)
            simulate_mouse_movement()
            
            # Simulate user taking a break
            if random.random() < 0.3:  # 30% chance of taking a break
                break_duration = random.uniform(30, 120)  # Break for 30 seconds to 2 minutes
                print(f"Taking a break for {break_duration:.2f} seconds...")
                time.sleep(break_duration)
            
            time.sleep(random.uniform(5, 15))  # Increased variation in delay between searches
    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
