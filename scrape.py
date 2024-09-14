import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time, random, os, pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException


def check_stupid_captcha(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')) #check iframe
        )
        print("Captcha detected!")
        return True
    except:
        print("No Captcha found!")
        return False

def solve_captcha_manually(driver):
    print("Solve the Captcha. Press Enter when done!")
    input()
    print("Resuming script")

def wait_for_element_to_appear(driver, element_selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_selector)) #wait for it
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {element_selector}")
        return None
    
def wait_for_clickable_element_to_appear(driver, element_selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, element_selector)) #wait for it
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for clickable element: {element_selector}")
        return None


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element) #scroll
    time.sleep(1)

def hover_over_element(driver, element_selector, retries=3):
    for attempt in range(retries):
        try:
            element = wait_for_element_to_appear(driver, element_selector) 
            if element:
                scroll_to_element(driver, element)
                actions = ActionChains(driver) #create a chain of actions
                actions.move_to_element(element).perform() #move the mouse to the element
                time.sleep(2)
                print(f"Successfully hovered over element: {element_selector}")
                return
            else:
                print(f"Element not found: {element_selector}")
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException encountered, retrying... (Attempt {attempt + 1}/{retries})")
        except Exception as e:
            print(f"Error in hover_over_element: {e}")
        
    print(f"Failed to hover over element after {retries} attempts: {element_selector}")


def drag_and_drop(driver, source_selector, target_selector):
    source = wait_for_element_to_appear(driver, source_selector)
    target = wait_for_element_to_appear(driver, target_selector)
    if source and target:
        try:
            scroll_to_element(driver, source) #scroll to ensure it is in view
            actions = ActionChains(driver) #create a chain of actions
            actions.click_and_hold(source).move_to_element(target).release().perform() #drag and drop
            print(f"Successfully performed drag and drop: {source_selector} to {target_selector}")
        except Exception as e:
            print(f"Error in drag_and_drop: {e}")
    else:
        print(f"Source or target element not found for drag and drop")
        
def right_click_element(driver, element_selector):
    max_attempts = 1
    for attempt in range(max_attempts):
        try:
            element = wait_for_clickable_element_to_appear(driver, element_selector)
            if element:
                scroll_to_element(driver, element)
                actions = ActionChains(driver)
                actions.context_click(element).perform()
                print(f"Successfully right-clicked element: {element_selector}")
                return
            else:
                print(f"Element not clickable: {element_selector}")
        except StaleElementReferenceException:
            print(f"Stale element reference, retrying... (Attempt {attempt + 1}/{max_attempts})")
        except ElementNotInteractableException:
            print(f"Element not interactable, retrying... (Attempt {attempt + 1}/{max_attempts})")
        except Exception as e:
            print(f"Error in right_click_element: {e}")
        
        if attempt < max_attempts - 1:
            time.sleep(2)  # Wait before retrying
    
    print(f"Failed to right-click element after {max_attempts} attempts: {element_selector}")


def mimic_human(driver, min_scroll=2, max_scroll=5):
    scroll_time = random.uniform(min_scroll, max_scroll)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll down
    time.sleep(scroll_time)

    scroll_up = random.uniform(1, 3)
    driver.execute_script("window.scrollBy(0, -300);") #scroll up
    time.sleep(scroll_up)
    print("Performed human-like scrolling")

def get_page_info(driver):
    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    
    tags = driver.find_elements(By.XPATH, "//*") #retrive all elements
    unique_tags = set(tag.tag_name for tag in tags) #store tags in a set
    print("Unique tags on the page:", ", ".join(unique_tags))
    
    elements_with_class_or_id = driver.find_elements(By.XPATH, "//*[@class or @id]")[:5] #retreive first 5 elements(class or id)
    print("Sample elements with class or id:")
    for elem in elements_with_class_or_id:
        print(f"Tag: {elem.tag_name}, Class: {elem.get_attribute('class')}, ID: {elem.get_attribute('id')}")
        
def scrape_website(url, headless=True):
    print("Launching Firefuck browser: ")

    firefox_driver_path = "geckodriver.exe"  # Firefuck web driver

    ua = UserAgent()  # Create an instance of UserAgent

    options = webdriver.FirefoxOptions()  # Create an instance of Firefox options
    options.set_preference("general.useragent.override", ua.random)  # Random to avoid being blocked

    if headless:
        options.add_argument('--headless')  # Run in headless mode

    # Configure Firefox to use Tor's SOCKS5 proxy
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9150)
    options.set_preference('network.proxy.socks_remote_dns', True)

    driver = webdriver.Firefox(service=Service(firefox_driver_path), options=options)

    try:
        driver.get(url)
        
        driver.delete_all_cookies()  # Clears all cookies before starting

        # Extract domain name from URL for cookies
        domain = driver.current_url.split("/")[2]
        cookies_file = f'{domain}_cookies.pkl'  # Save cookies specific to the domain

        if os.path.exists(cookies_file):
            with open(cookies_file, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    # Add only cookies matching the current domain
                    if domain in cookie.get('domain', ''):
                        try:
                            driver.add_cookie(cookie)
                        except Exception as e:
                            print(f"Could not add cookie: {e}")

        driver.get(url)  # Reload the page to apply cookies

        if check_stupid_captcha(driver):
            print("Switching to non-headless mode for manual captcha solving...")
            driver.quit()  # Quit the current driver

            # Switch to non-headless mode
            options.remove_argument('--headless')
            driver = webdriver.Firefox(service=Service(firefox_driver_path), options=options)

            driver.get(url)
            driver.delete_all_cookies()
            
            if os.path.exists(cookies_file):
                with open(cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        if domain in cookie.get('domain', ''):
                            try:
                                driver.add_cookie(cookie)
                            except Exception as e:
                                print(f"Could not add cookie: {e}")

            driver.get(url)  # Reload the page to apply cookies
            solve_captcha_manually(driver)
            # Switch back to headless mode after solving the captcha
            print("Switching back to headless mode...")
            driver.quit()  # Quit the current driver
            
            options.add_argument('--headless')
            driver = webdriver.Firefox(service=Service(firefox_driver_path), options=options)

            driver.get(url)
            driver.delete_all_cookies()
            
            if os.path.exists(cookies_file):
                with open(cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        if domain in cookie.get('domain', ''):
                            try:
                                driver.add_cookie(cookie)
                            except Exception as e:
                                print(f"Could not add cookie: {e}")

            driver.get(url)  # Reload the page to apply cookies

        get_page_info(driver)

        hover_over_element(driver, 'a:not([href=""])')

        mimic_human(driver)

        drag_and_drop(driver, '.thumbnail', '.caption')

        mimic_human(driver)

        right_click_element(driver, 'button.btn-success:not([style*="display:none"]):not([style*="display: none"])')

        mimic_human(driver)

        html = driver.page_source

        # Save cookies for future sessions
        cookies = driver.get_cookies()
        with open(cookies_file, 'wb') as f:
            pickle.dump(cookies, f)

        return html
    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        driver.quit()



#get html
def extract_body_content(html_content):
    if html_content is None:
        print("No HTML content")
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser") #parse in soup
    body_content = soup.body #get <body> content

    if body_content:
        return str(body_content)
    else:
        return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Remove all <script> and <style> tags
    for tag in soup(["script", "style"]):
        tag.extract()
    
    # Get the text content
    cleaned_content = soup.get_text(separator="\n")
    
    # Clean the lines, removing excess whitespace
    lines = cleaned_content.splitlines()

    filtered_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            filtered_lines.append(stripped_line)

    cleaned_content = "\n".join(filtered_lines)

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    chunks = []
    
    # Split the DOM content into chunks of max_length
    for i in range(0, len(dom_content), max_length):
        chunk = dom_content[i:i + max_length]
        chunks.append(chunk)

    return chunks
