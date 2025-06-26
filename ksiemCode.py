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
import re

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
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.results = []

    def open_chrome(self):
        try:
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

def extract_status_from_text(text):
    """Extract status from text (closed, resolved, on-hold)"""
    status_pattern = re.compile(r'(closed|resolved|on-hold)', re.IGNORECASE)
    match = status_pattern.search(text)
    return match.group(1).lower() if match else ""

def extract_dates_from_text(text):
    """Extract all dates from text"""
    date_pattern = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b')
    return date_pattern.findall(text)

def process_url(driver, url, output_file):
    """Process a single URL and extract required data"""
    result = {
        'original_url': url,
        'extracted_url': "",
        'status': "",
        'created_date': "",
        'closing_date': "",
        'all_dates_found': "",
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': "failed",  # Default status
        'error_message': ""
    }
    
    try:
        validated_url = validate_url(url)
        print(f"\nProcessing URL: {validated_url}")
        result['original_url'] = validated_url

        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(validated_url)
        time.sleep(10)  # Wait for page to load

        # Get all page text
        page_text = driver.find_element(By.TAG_NAME, 'body').text

        # Extract URL from page text
        url_pattern = re.compile(r'https?://[^\s]+')
        extracted_urls = url_pattern.findall(page_text)
        result['extracted_url'] = extracted_urls[0] if extracted_urls else ""

        # Extract status
        result['status'] = extract_status_from_text(page_text)

        # Extract dates
        dates = extract_dates_from_text(page_text)
        result['created_date'] = dates[0] if len(dates) > 0 else ""
        result['closing_date'] = dates[1] if len(dates) > 1 else ""
        result['all_dates_found'] = " | ".join(dates)
        
        # Mark as successful
        result['status'] = "success"
        result['error_message'] = ""

        print(f"Successfully processed: {validated_url}")

    except Exception as e:
        error_msg = f"Error processing URL {url}: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        result['status'] = "failed"
        result['error_message'] = error_msg
        
    finally:
        # Ensure we save the result even if there was an error
        save_single_result(result, output_file)
        
        # Ensure we return to main tab even if error occurs
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        return result

def save_single_result(result, output_file):
    """Save a single result to the output file, creating the file if it doesn't exist"""
    try:
        # Check if file exists to determine if we need headers
        file_exists = os.path.isfile(output_file)
        
        # Convert result to DataFrame
        df = pd.DataFrame([result])
        
        # If file exists, read it first to avoid duplicates
        if file_exists:
            existing_df = pd.read_csv(output_file)
            df = pd.concat([existing_df, df], ignore_index=True)
            # Remove duplicates based on original_url
            df = df.drop_duplicates(subset=['original_url'], keep='last')
        
        # Save to CSV
        df.to_csv(output_file, index=False)
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
                
            process_url(scraper.driver, url, output_file)
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