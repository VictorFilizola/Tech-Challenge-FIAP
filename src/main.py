from fastapi import FastAPI, HTTPException
from src.scraper import scrape_amazon_bestsellers
from src.analysis import (
    load_local_data,
    generate_general_analysis,
    generate_pricing_analysis,
    generate_authors_analysis,
    generate_engagement_analysis
)
import os
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI(
    title="Amazon Bestsellers API",
    description="API to scrape Amazon bestselling books and provide specific analytical views.",
    version="1.0.0"
)

@app.get("/health", tags=["System"])
def health_check():
    """Returns the operational status of the API."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info", tags=["System"])
def api_info():
    """Returns metadata about the locally cached data."""
    file_path = "data/bestsellers.json"
    if os.path.exists(file_path):
        last_modified = os.path.getmtime(file_path)
        last_scraped = datetime.fromtimestamp(last_modified).isoformat()
        return {"data_available": True, "last_scraped_at": last_scraped}
    return {"data_available": False, "last_scraped_at": None}

@app.post("/api/scrape", tags=["Scraper"])
def trigger_scraper():
    """
    Triggers the Selenium scraper to fetch the latest data from Amazon and cache it locally.
    """
    try:
        data = scrape_amazon_bestsellers()
        return {"status": "success", "message": f"Successfully scraped and saved {len(data)} books."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/books", tags=["Data"])
def get_bestseller_books():
    """
    Retrieves the raw list of books instantly from the local JSON cache.
    """
    data = load_local_data()
    if not data:
        raise HTTPException(status_code=404, detail="No data found. Please call POST /api/scrape first.")
    return {"status": "success", "total": len(data), "data": data}

@app.get("/api/analysis/general", tags=["Analytics"])
def get_general_analysis():
    """Returns general descriptive statistics about the bestsellers list."""
    analysis = generate_general_analysis()
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return {"status": "success", "data": analysis}

@app.get("/api/analysis/pricing", tags=["Analytics"])
def get_pricing_analysis():
    """Returns a detailed breakdown of pricing distributions and outliers."""
    analysis = generate_pricing_analysis()
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return {"status": "success", "data": analysis}

@app.get("/api/analysis/authors", tags=["Analytics"])
def get_authors_analysis():
    """Returns metrics on author market share and dominance."""
    analysis = generate_authors_analysis()
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return {"status": "success", "data": analysis}

@app.get("/api/analysis/engagement", tags=["Analytics"])
def get_engagement_analysis():
    """Returns engagement metrics based on review counts and ratings."""
    analysis = generate_engagement_analysis()
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return {"status": "success", "data": analysis}