# # import os
# # import time
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import WebDriverException
# # from dotenv import load_dotenv, find_dotenv
# # import pandas as pd
# # from urllib.parse import urlparse
# # import traceback

# # # Improved environment file handling
# # dotenv_path = find_dotenv()
# # if not dotenv_path:
# #     raise FileNotFoundError("Could not find .env file")

# # print(f"Loading environment variables from: {dotenv_path}")
# # load_dotenv(dotenv_path)

# # class ServiceCheck:
# #     def __init__(self):
# #         options = webdriver.ChromeOptions()
# #         options.add_argument('--no-sandbox')
# #         options.add_argument('--disable-dev-shm-usage')
# #         self.driver = webdriver.Chrome(options=options)

# #     def open_chrome(self):
# #         try:
# #             self.driver.maximize_window()
# #             return True
# #         except WebDriverException as e:
# #             print(f"Failed to open Chrome: {e}")
# #             return False

# #     def close_extra_tabs(self):
# #         """Close all tabs except the first login tab."""
# #         while len(self.driver.window_handles) > 1:
# #             self.driver.switch_to.window(self.driver.window_handles[-1])
# #             self.driver.close()
# #         self.driver.switch_to.window(self.driver.window_handles[0])

# #     def done(self):
# #         self.driver.quit()

# # def get_env_var(name):
# #     """Get and validate environment variable"""
# #     value = os.getenv(name)
# #     if not value:
# #         raise ValueError(f"Missing required environment variable: {name}")
# #     return value

# # def validate_url(url):
# #     """Validate and clean the URL with extensive checks"""
# #     print(f"Validating URL: {url} (type: {type(url)})")
    
# #     if url is None:
# #         raise ValueError("URL is None")
    
# #     if not isinstance(url, str):
# #         if hasattr(url, '__str__'):
# #             url = str(url)
# #         else:
# #             raise ValueError(f"URL must be a string, got {type(url)} instead")
    
# #     url = url.strip()
# #     if not url:
# #         raise ValueError("URL is empty")
    
# #     if url.lower() in ['nan', 'nat', 'none', 'null']:
# #         raise ValueError(f"URL appears to be placeholder: {url}")
    
# #     if not url.startswith(('http://', 'https://')):
# #         url = 'https://' + url
        
# #     parsed = urlparse(url)
# #     if not all([parsed.scheme, parsed.netloc]):
# #         raise ValueError(f"Invalid URL format: {url}")
    
# #     return url

# # def automate_login(driver):
# #     """Log in to KSIEM system using credentials from .env file."""
# #     try:
# #         ks_username = get_env_var('KS_USERNAME')
# #         ks_password = get_env_var('KS_PASSWORD')
# #         ks_url = get_env_var('KS_SITEURL')
        
# #         print(f"Attempting to navigate to: {ks_url}")
# #         driver.get(ks_url)
# #         time.sleep(3)

# #         # Enter username
# #         username_field = WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.CLASS_NAME, "input-block")))
# #         username_field.send_keys(ks_username)
        
# #         # Enter password
# #         password_field = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/label[2]/input')
# #         password_field.send_keys(ks_password)
        
# #         # Click login
# #         login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/p[1]/input')
# #         login_button.click()
# #         time.sleep(5)

# #         # Verify login success
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/ul/li[2]')))
        
# #         print("Login successful")

# #     except Exception as e:
# #         print(f"An error occurred during login: {e}")
# #         raise

# # def process_first_url(driver, url):
# #     """Open a URL in a new tab and wait for 1 minute"""
# #     try:
# #         validated_url = validate_url(url)
# #         print(f"Final validated URL: {validated_url}")
        
# #         # Open new tab
# #         driver.execute_script("window.open('');")
# #         driver.switch_to.window(driver.window_handles[-1])
        
# #         # Navigate to URL
# #         print(f"Attempting to visit URL: {validated_url}")
# #         driver.get(validated_url)
        
# #         # Wait for 1 minute (60 seconds)
# #         print("Waiting for 60 seconds...")
# #         time.sleep(3360)
        
# #         # Close the tab
# #         driver.close()
# #         driver.switch_to.window(driver.window_handles[0])
# #         print("URL processing complete")
        
# #     except Exception as e:
# #         print(f"Error processing URL: {e}")
# #         raise

# # def get_first_url_from_csv(file_path):
# #     """Extract the first URL from CSV file with extensive validation"""
# #     try:
# #         print(f"Reading CSV file: {file_path}")
# #         df = pd.read_csv(file_path)
        
# #         # Debug: Print all columns and first few rows
# #         print("\nAvailable columns:", df.columns.tolist())
# #         print("\nFirst 3 rows of data:")
# #         print(df.head(3))
        
# #         # Find the ticket link column (case insensitive)
# #         ticket_col = next((col for col in df.columns 
# #                          if 'url' in col.lower()), None)
        
# #         if not ticket_col:
# #             raise ValueError("No 'Ticket link' column found in CSV file")
            
# #         print(f"\nFound ticket column: {ticket_col}")
# #         urls = df[ticket_col].dropna()
        
# #         if len(urls) == 0:
# #             raise ValueError("No URLs found in the CSV file")
            
# #         first_url = urls.iloc[0]
# #         print(f"\nRaw URL extracted: {first_url} (type: {type(first_url)})")
        
# #         return first_url
            
# #     except Exception as e:
# #         print(f"Error reading CSV file: {e}")
# #         raise

# # if __name__ == '__main__':
# #     try:
# #         # Validate all required environment variables first
# #         required_vars = ['KS_USERNAME', 'KS_PASSWORD', 'KS_SITEURL']
# #         for var in required_vars:
# #             get_env_var(var)  # Will raise error if missing
            
# #         # Initialize browser
# #         print("Initializing browser...")
# #         service_check = ServiceCheck()
# #         if not service_check.open_chrome():
# #             raise RuntimeError("Failed to initialize browser")
        
# #         # Step 1: Login
# #         print("\nStarting login process...")
# #         automate_login(service_check.driver)
        
# #         # Step 2: Get first URL from CSV
# #         csv_file = "extracted_urls.csv"  # Change to your CSV file path
# #         print(f"\nExtracting URL from: {csv_file}")
# #         first_url = get_first_url_from_csv(csv_file)
# #         print(f"\nExtracted URL before validation: {first_url}")
        
# #         # Step 3: Process the URL
# #         print("\nProcessing URL...")
# #         process_first_url(service_check.driver, first_url)
        
# #         print("\nReady for next stage...")
        
# #         # Keep browser open for next steps
# #         input("Press Enter to exit...")
        
# #     except Exception as e:
# #         print(f"\nFatal error: {e}")
# #         traceback.print_exc()
# #     finally:
# #         print("\nCleaning up...")
# #         if 'service_check' in locals():
# #             service_check.done()





# import os
# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, WebDriverException
# from dotenv import load_dotenv, find_dotenv
# from urllib.parse import urlparse
# import traceback
# from datetime import datetime

# # Environment setup
# dotenv_path = find_dotenv()
# if not dotenv_path:
#     raise FileNotFoundError("Could not find .env file")
# load_dotenv(dotenv_path)

# class WebScraper:
#     def __init__(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         self.driver = webdriver.Chrome(options=options)
#         self.results = []

#     def open_chrome(self):
#         try:
#             self.driver.maximize_window()
#             return True
#         except WebDriverException as e:
#             print(f"Failed to open Chrome: {e}")
#             return False

#     def close_extra_tabs(self):
#         """Close all tabs except the first one."""
#         while len(self.driver.window_handles) > 1:
#             self.driver.switch_to.window(self.driver.window_handles[-1])
#             self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[0])

#     def done(self):
#         self.driver.quit()

# def get_env_var(name):
#     """Get and validate environment variable"""
#     value = os.getenv(name)
#     if not value:
#         raise ValueError(f"Missing required environment variable: {name}")
#     return value

# def validate_url(url):
#     """Validate and clean URL"""
#     if not isinstance(url, str):
#         url = str(url)
#     url = url.strip()
#     if not url:
#         raise ValueError("URL is empty")
#     if not url.startswith(('http://', 'https://')):
#         url = 'https://' + url
#     return url

# def login(driver):
#     """Log in to KSIEM system"""
#     try:
#         username = get_env_var('KS_USERNAME')
#         password = get_env_var('KS_PASSWORD')
#         site_url = get_env_var('KS_SITEURL')
        
#         driver.get(site_url)
#         time.sleep(3)

#         # Enter credentials
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "input-block"))).send_keys(username)
#         driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/label[2]/input').send_keys(password)
#         driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/p[1]/input').click()
#         time.sleep(5)

#         # Verify login
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/ul/li[2]')))
#         print("Login successful")

#     except Exception as e:
#         print(f"Login failed: {e}")
#         raise

# def extract_element_text(driver, xpath, default=""):
#     """Safely extract text from an element if it exists"""
#     try:
#         return driver.find_element(By.XPATH, xpath).text.strip()
#     except NoSuchElementException:
#         return default

# def process_url(driver, url, results):
#     """Process a single URL and extract required data"""
#     try:
#         validated_url = validate_url(url)
#         print(f"\nProcessing URL: {validated_url}")

#         # Open new tab
#         driver.execute_script("window.open('');")
#         driver.switch_to.window(driver.window_handles[-1])
#         driver.get(validated_url)
#         time.sleep(5)  # Wait for page to load

#         # Extract data
#         url_text = extract_element_text(
#             driver, 
#             '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[5]/div[2]'
#         )
#         created_date = extract_element_text(
#             driver,
#             '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[3]/table[1]/tbody/tr[5]/td[2]'
#         )
#         closing_date = extract_element_text(
#             driver,
#             '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[3]/table[1]/tbody/tr[6]/td[2]'
#         )
#         optional_field = extract_element_text(
#             driver,
#             '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[2]'
#         )

#         # Store results
#         results.append({
#             'original_url': validated_url,
#             'extracted_url': url_text,
#             'created_date': created_date,
#             'closing_date': closing_date,
#             'optional_field': optional_field,
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         })

#         # Close tab
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         print(f"Successfully processed: {validated_url}")

#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#         traceback.print_exc()
#         # Ensure we return to main tab even if error occurs
#         if len(driver.window_handles) > 1:
#             driver.close()
#         driver.switch_to.window(driver.window_handles[0])

# def get_urls_from_csv(file_path):
#     """Extract URLs from CSV file"""
#     try:
#         df = pd.read_csv(file_path)
        
#         # Find ticket link column (case insensitive)
#         ticket_col = next((col for col in df.columns if 'url' in col.lower()), None)
#         if not ticket_col:
#             raise ValueError("No 'Ticket link' column found in CSV")
            
#         urls = df[ticket_col].dropna().unique()
#         if len(urls) == 0:
#             raise ValueError("No URLs found in CSV file")
            
#         return urls
            
#     except Exception as e:
#         print(f"Error reading CSV file: {e}")
#         raise

# def save_results(results, output_file="extracted_data.csv"):
#     """Save extracted data to CSV"""
#     if not results:
#         print("No results to save")
#         return
    
#     df = pd.DataFrame(results)
#     df.to_csv(output_file, index=False)
#     print(f"\nSuccessfully saved {len(results)} records to {output_file}")

# def main():
#     try:
#         # Initialize
#         scraper = WebScraper()
#         if not scraper.open_chrome():
#             raise RuntimeError("Failed to initialize browser")
        
#         # Login
#         login(scraper.driver)
        
#         # Get URLs
#         urls = get_urls_from_csv("extracted_urls.csv")
#         print(f"\nFound {len(urls)} URLs to process")
        
#         # Process each URL
#         for url in urls:
#             process_url(scraper.driver, url, scraper.results)
#             time.sleep(5)  # Brief pause between URLs
        
#         # Save results
#         save_results(scraper.results)
        
#         print("\nProcessing complete")
        
#     except Exception as e:
#         print(f"\nFatal error: {e}")
#         traceback.print_exc()
#     finally:
#         print("\nCleaning up...")
#         if 'scraper' in locals():
#             scraper.done()

# if __name__ == '__main__':
#     main()








import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse
import traceback
from datetime import datetime

# Environment setup
dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Could not find .env file")
load_dotenv(dotenv_path)

class WebScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.results = []

    def open_chrome(self):
        try:
            self.driver.maximize_window()
            return True
        except WebDriverException as e:
            print(f"Failed to open Chrome: {e}")
            return False

    def close_extra_tabs(self):
        """Close all tabs except the first one."""
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def done(self):
        self.driver.quit()

def get_env_var(name):
    """Get and validate environment variable"""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

def validate_url(url):
    """Validate and clean URL"""
    if not isinstance(url, str):
        url = str(url)
    url = url.strip()
    if not url:
        raise ValueError("URL is empty")
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def login(driver):
    """Log in to KSIEM system"""
    try:
        username = get_env_var('KS_USERNAME')
        password = get_env_var('KS_PASSWORD')
        site_url = get_env_var('KS_SITEURL')
        
        driver.get(site_url)
        time.sleep(3)

        # Enter credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "input-block"))).send_keys(username)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/label[2]/input').send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div/div[2]/form/p[1]/input').click()
        time.sleep(5)

        # Verify login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/ul/li[2]')))
        print("Login successful")

    except Exception as e:
        print(f"Login failed: {e}")
        raise

def extract_element_text(driver, xpath, default=""):
    """Safely extract text from an element if it exists"""
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except NoSuchElementException:
        return default

def process_url(driver, url, results, output_file):
    """Process a single URL and extract required data"""
    try:
        validated_url = validate_url(url)
        print(f"\nProcessing URL: {validated_url}")

        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(validated_url)
        time.sleep(10)  # Wait for page to load

        # Extract data
        url_text = extract_element_text(
            driver, 
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[5]/div[2]'
        )
        created_date = extract_element_text(
            driver,
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[3]/table[1]/tbody/tr[5]/td[2]'
        )
        closing_date = extract_element_text(
            driver,
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[3]/table[1]/tbody/tr[6]/td[2]'
        )
        optional_field = extract_element_text(
            driver,
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[2]'
        )

        # Create result dictionary
        result = {
            'original_url': validated_url,
            'extracted_url': url_text,
            'created_date': created_date,
            'closing_date': closing_date,
            'optional_field': optional_field,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Append to results list
        results.append(result)
        
        # Immediately save this result to the output file
        save_single_result(result, output_file)

        # Close tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Successfully processed: {validated_url}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        traceback.print_exc()
        # Ensure we return to main tab even if error occurs
        if len(driver.window_handles) > 1:
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

def save_single_result(result, output_file):
    """Save a single result to the output file, creating the file if it doesn't exist"""
    try:
        # Check if file exists to determine if we need headers
        file_exists = os.path.isfile(output_file)
        
        # Convert result to DataFrame
        df = pd.DataFrame([result])
        
        # Append to CSV (create if doesn't exist)
        df.to_csv(output_file, mode='a', header=not file_exists, index=False)
        
        print(f"Saved result for {result['original_url']} to {output_file}")
    except Exception as e:
        print(f"Error saving result to file: {e}")
        traceback.print_exc()

def get_urls_from_csv(file_path):
    """Extract URLs from CSV file"""
    try:
        df = pd.read_csv(file_path)
        
        # Find ticket link column (case insensitive)
        ticket_col = next((col for col in df.columns if 'url' in col.lower()), None)
        if not ticket_col:
            raise ValueError("No 'Ticket link' column found in CSV")
            
        urls = df[ticket_col].dropna().unique()
        if len(urls) == 0:
            raise ValueError("No URLs found in CSV file")
            
        return urls
            
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        raise

def save_results(results, output_file="extracted_data.csv"):
    """Save extracted data to CSV (for final save)"""
    if not results:
        print("No results to save")
        return
    
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"\nSuccessfully saved {len(results)} records to {output_file}")

def get_processed_urls(output_file):
    """Get URLs that have already been processed from the output file"""
    if not os.path.exists(output_file):
        return set()
    
    try:
        df = pd.read_csv(output_file)
        return set(df['original_url'].dropna().unique())
    except Exception as e:
        print(f"Warning: Could not read processed URLs from {output_file}: {e}")
        return set()

def main():
    output_file = "extracted_data.csv"
    try:
        # Initialize
        scraper = WebScraper()
        if not scraper.open_chrome():
            raise RuntimeError("Failed to initialize browser")
        
        # Login
        login(scraper.driver)
        
        # Get URLs
        urls = get_urls_from_csv("extracted_urls.csv")
        print(f"\nFound {len(urls)} URLs to process")
        
        # Get URLs that have already been processed
        processed_urls = get_processed_urls(output_file)
        if processed_urls:
            print(f"Found {len(processed_urls)} previously processed URLs")
        
        # Process each URL that hasn't been processed yet
        for url in urls:
            if url in processed_urls:
                print(f"Skipping already processed URL: {url}")
                continue
                
            process_url(scraper.driver, url, scraper.results, output_file)
            time.sleep(5)  # Brief pause between URLs
        
        print("\nProcessing complete")
        
    except Exception as e:
        print(f"\nFatal error: {e}")
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        if 'scraper' in locals():
            scraper.done()

if __name__ == '__main__':
    main()