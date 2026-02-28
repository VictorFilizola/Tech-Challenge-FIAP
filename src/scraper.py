import json
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_amazon_bestsellers():
    books_data = []
    
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edge/120.0.0.0")
    
    driver = webdriver.Edge(options=edge_options)
    
    try:
        for page_num in range(1, 3):
            url = f"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_{page_num}_books?_encoding=UTF8&pg={page_num}"
            driver.get(url)
            
            for _ in range(10):
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.5)
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "gridItemRoot"))
            )
            
            items = driver.find_elements(By.ID, "gridItemRoot")
            
            for item in items:
                try:
                    title_elements = item.find_elements(By.CSS_SELECTOR, "div._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
                    title = title_elements[0].text.strip() if title_elements else "Unknown Title"
                    
                    author_elements = item.find_elements(By.CSS_SELECTOR, "a.a-size-small")
                    author = author_elements[0].text.strip() if author_elements else "Unknown Author"
                    
                    rating_elements = item.find_elements(By.CSS_SELECTOR, "span.a-icon-alt")
                    rating = rating_elements[0].get_attribute("innerHTML").strip() if rating_elements else "No Rating"
                    
                    # Extracting Rating Count
                    icon_row = item.find_elements(By.CSS_SELECTOR, "div.a-icon-row")
                    if icon_row:
                        count_elements = icon_row[0].find_elements(By.CSS_SELECTOR, "span.a-size-small")
                        rating_count = count_elements[0].text.strip() if count_elements else "0"
                    else:
                        rating_count = "0"
                    
                    price_elements = item.find_elements(By.CSS_SELECTOR, "span._cDEzb_p13n-sc-price_3mJ9Z")
                    price = price_elements[0].text.strip() if price_elements else "$0.00"
                    
                    books_data.append({
                        "title": title,
                        "author": author,
                        "rating": rating,
                        "rating_count": rating_count,
                        "price": price
                    })
                except Exception:
                    continue
                    
    finally:
        driver.quit()
        
    # Save the data locally to a JSON file
    os.makedirs("data", exist_ok=True)
    with open("data/bestsellers.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, indent=4, ensure_ascii=False)
        
    return books_data