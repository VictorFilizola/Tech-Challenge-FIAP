import requests
from bs4 import BeautifulSoup

def scrape_amazon_bestsellers():
    # Target URL
    url = "https://www.amazon.com/gp/bestsellers/books/"
    
    # Headers to simulate a real browser request and avoid 503 errors
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Amazon. Status code: {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    books_data = []
    
    # Find the main container for the items. 
    # Note: Amazon changes these classes frequently. You may need to inspect the live DOM.
    items = soup.find_all("div", id="gridItemRoot")
    
    for item in items:
        try:
            # Extracting Title
            title_element = item.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
            title = title_element.text.strip() if title_element else "Unknown Title"
            
            # Extracting Author
            author_element = item.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y") 
            # Often, author is the second instance of this class or an 'a' tag nearby
            author = item.find("a", class_="a-size-small").text.strip() if item.find("a", class_="a-size-small") else "Unknown Author"
            
            # Extracting Rating
            rating_element = item.find("span", class_="a-icon-alt")
            rating = rating_element.text.strip() if rating_element else "No Rating"
            
            # Extracting Price
            price_element = item.find("span", class_="_cDEzb_p13n-sc-price_3mJ9Z")
            price = price_element.text.strip() if price_element else "$0.00"
            
            books_data.append({
                "title": title,
                "author": author,
                "rating": rating,
                "price": price
            })
        except AttributeError:
            continue
            
    return books_data