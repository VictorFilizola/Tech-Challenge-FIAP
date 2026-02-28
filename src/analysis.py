import pandas as pd

def generate_descriptive_analysis(books_data):
    if not books_data:
        return {"error": "No data available to analyze."}
        
    # Load data into a pandas DataFrame
    df = pd.DataFrame(books_data)
    
    # Clean the 'price' column (remove '$' and convert to float)
    df['price_cleaned'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Clean the 'rating' column (extract just the number, e.g., "4.8 out of 5 stars" -> 4.8)
    df['rating_cleaned'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)
    
    # Calculate descriptive statistics
    total_books = len(df)
    average_price = df['price_cleaned'].mean()
    average_rating = df['rating_cleaned'].mean()
    
    # Find the most frequent authors in the best sellers list
    top_authors = df['author'].value_counts().head(5).to_dict()
    
    # Prepare the analytical payload
    analysis_result = {
        "total_books_analyzed": total_books,
        "average_price_usd": round(average_price, 2) if pd.notna(average_price) else 0.0,
        "average_rating": round(average_rating, 2) if pd.notna(average_rating) else 0.0,
        "authors_with_multiple_bestsellers": top_authors
    }
    
    return analysis_result