import pandas as pd
import json

def load_local_data():
    """Helper function to load the cached JSON data."""
    try:
        with open("data/bestsellers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_cleaned_dataframe():
    """Loads local data and returns a cleaned pandas DataFrame for analysis."""
    books_data = load_local_data()
    if not books_data:
        return None
        
    df = pd.DataFrame(books_data)
    
    # Clean the 'price' column (remove '$' and convert to float)
    df['price_cleaned'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Clean the 'rating' column (extract just the number)
    df['rating_cleaned'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)
    
    # Clean rating count (e.g., "43,124" -> 43124.0)
    df['rating_count_cleaned'] = df['rating_count'].str.replace(',', '').str.replace('.', '').astype(float).fillna(0)
    
    return df

def generate_general_analysis():
    """Calculates high-level general statistics."""
    df = get_cleaned_dataframe()
    if df is None:
        return {"error": "No local data found. Please trigger the scraper first."}
        
    total_books = len(df)
    average_rating = df['rating_cleaned'].mean()
    total_reviews = df['rating_count_cleaned'].sum()
    
    return {
        "total_books_analyzed": total_books,
        "average_rating": round(average_rating, 2) if pd.notna(average_rating) else 0.0,
        "total_reviews_across_all_books": int(total_reviews)
    }

def generate_pricing_analysis():
    """Calculates pricing distribution, median, and outliers."""
    df = get_cleaned_dataframe()
    if df is None:
        return {"error": "No local data found."}
        
    prices = df['price_cleaned'].dropna()
    if prices.empty:
        return {"error": "No price data available to analyze."}
        
    return {
        "average_price": round(prices.mean(), 2),
        "median_price": round(prices.median(), 2),
        "cheapest_book_price": round(prices.min(), 2),
        "most_expensive_book_price": round(prices.max(), 2),
        "cheapest_25_percent_under": round(prices.quantile(0.25), 2),
        "top_25_percent_above": round(prices.quantile(0.75), 2)
    }

def generate_authors_analysis():
    """Calculates author dominance and market share."""
    df = get_cleaned_dataframe()
    if df is None:
        return {"error": "No local data found."}
        
    total_books = len(df)
    author_counts = df['author'].value_counts()
    top_authors = author_counts.head(5).to_dict()
    
    # Calculate market share of the top 5 authors
    top_5_total_books = sum(top_authors.values())
    market_share = (top_5_total_books / total_books) * 100 if total_books > 0 else 0
    
    return {
        "unique_authors_in_top_100": len(author_counts),
        "top_5_authors_by_book_count": top_authors,
        "top_5_authors_market_share_percentage": round(market_share, 2)
    }

def generate_engagement_analysis():
    """Calculates review concentration and hype vs quality metrics."""
    df = get_cleaned_dataframe()
    if df is None:
        return {"error": "No local data found."}
        
    # Top 5 most reviewed books (Highest Engagement)
    most_reviewed = df.nlargest(5, 'rating_count_cleaned')
    most_reviewed_list = most_reviewed[['title', 'rating_count_cleaned']].to_dict('records')
    
    # High Quality + High Engagement (Books rated >= 4.8 sorted by review count)
    high_quality = df[df['rating_cleaned'] >= 4.8]
    top_high_quality = high_quality.nlargest(5, 'rating_count_cleaned')
    top_high_quality_list = top_high_quality[['title', 'rating_cleaned', 'rating_count_cleaned']].to_dict('records')
    
    return {
        "most_reviewed_books": most_reviewed_list,
        "highest_rated_with_high_engagement": top_high_quality_list
    }