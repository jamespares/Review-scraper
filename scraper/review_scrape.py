from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_trustpilot_reviews(url, num_pages):
    # Set up the Chrome driver
    service = Service('path_to_chromedriver')  # Update with the actual path to your ChromeDriver
    driver = webdriver.Chrome(service=service)
    
    reviews = []

    for page in range(1, num_pages + 1):
        # Navigate to each page
        driver.get(f"{url}?page={page}")
        
        # Wait until the review elements are loaded (adjust the time if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.review-card'))
        )
        time.sleep(2)  # Small sleep to ensure everything is loaded
        
        # Locate the review elements
        review_elements = driver.find_elements(By.CSS_SELECTOR, '.review-card')
        
        # Iterate through each review
        for element in review_elements:
            try:
                # Scrape the necessary fields
                rating = element.find_element(By.CSS_SELECTOR, '.star-rating').get_attribute('data-rating')
                title = element.find_element(By.CSS_SELECTOR, '.review-content__title').text
                body = element.find_element(By.CSS_SELECTOR, '.review-content__text').text
                date = element.find_element(By.CSS_SELECTOR, '.review-content-header__dates').text
                
                reviews.append({'Rating': rating, 'Title': title, 'Body': body, 'Date': date})
            except Exception as e:
                print(f"Error scraping review: {e}")
                continue

    driver.quit()
    return pd.DataFrame(reviews)

# Example usage:
visahq_reviews = scrape_trustpilot_reviews('https://uk.trustpilot.com/review/www.visahq.com', num_pages=10)
ivisa_reviews = scrape_trustpilot_reviews('https://uk.trustpilot.com/review/ivisa.com', num_pages=10)

# Save the data to CSV
visahq_reviews.to_csv('visahq_reviews.csv', index=False)
ivisa_reviews.to_csv('ivisa_reviews.csv', index=False)