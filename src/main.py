from fastapi import FastAPI, HTTPException
from scraper import scrape_amazon_bestsellers
from analysis import generate_descriptive_analysis

# Initialize the FastAPI app
app = FastAPI(
    title="Amazon Bestsellers API",
    description="API to scrape Amazon bestselling books and provide descriptive analysis.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Amazon Bestsellers API. Navigate to /docs for documentation."}

@app.get("/api/books", tags=["Scraper"])
def get_bestseller_books():
    """
    Scrapes the current Amazon Best Sellers in Books and returns the list.
    """
    try:
        data = scrape_amazon_bestsellers()
        if not data:
            raise HTTPException(status_code=404, detail="Could not retrieve books. CSS selectors might need updating.")
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis", tags=["Analytics"])
def get_books_analysis():
    """
    Scrapes the data and returns a descriptive analysis of the current best sellers.
    """
    try:
        data = scrape_amazon_bestsellers()
        if not data:
            raise HTTPException(status_code=404, detail="Could not retrieve data for analysis.")
            
        analysis = generate_descriptive_analysis(data)
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))