import os
import pandas as pd
from google_play_scraper import Sort, reviews

def scrape_bank_reviews(app_id: str, bank_name: str, count_target: int = 500):
    """
    Scrapes targeted mobile banking reviews.
    Explicitly targets 'lang=en' and 'country=et' to pull localized Ethiopian store feedback.
    """
    print(f"[*] Extracting raw feedback for {bank_name} using ID: {app_id}...")
    
    all_parsed_reviews = []
    continuation_token = None
    
    # Use a loop with explicit tokens to navigate store pagination boundaries safely
    while len(all_parsed_reviews) < count_target:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',        # Keep 'en' to filter out non-English reviews for NLP tasks
                country='et',     # CRITICAL FIX: Direct the engine to search the Ethiopian store region
                sort=Sort.NEWEST,
                count=100,        # Pull in optimal batches of 100 entries per loop iteration
                continuation_token=continuation_token
            )
            
            if not result:
                # Break if the app store runs out of records entirely
                break
                
            for r in result:
                all_parsed_reviews.append({
                    'review_id': r.get('reviewId'),
                    'review_text': r.get('content'),
                    'rating': r.get('score'),
                    'date': r.get('at'),
                    'bank': bank_name,
                    'source': 'Google Play'
                })
                
            # If no continuation token is returned by Google, we have reached the end
            if not continuation_token:
                break
                
        except Exception as e:
            print(f"[X] Runtime error during batch extraction for {bank_name}: {str(e)}")
            break

    df = pd.DataFrame(all_parsed_reviews)
    # Truncate to your target size to avoid inflating data weights
    if len(df) > count_target:
        df = df.head(count_target)
        
    print(f"[✓] Extracted {len(df)} records for {bank_name}.")
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resolves data quality issues: Deduplication, Missing Fields, and Date Normalization.
    """
    if df.empty:
        return df
    
    initial_count = len(df)
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=['review_id'])
    dup_drop_count = initial_count - len(df)
    
    # 2. Missing Core Values
    df = df.dropna(subset=['review_text', 'rating'])
    df['review_text'] = df['review_text'].astype(str).str.strip()
    df = df[df['review_text'] != ""]
    null_drop_count = initial_count - dup_drop_count - len(df)
    
    # 3. Date Normalization
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    print(f"[i] Data Cleansing Ledger | Duplicates Dropped: {dup_drop_count} | Nulls Dropped: {null_drop_count} | Final Clean Count: {len(df)}")
    return df[['review_id', 'review_text', 'rating', 'date', 'bank', 'source']]

if __name__ == "__main__":
    # Standardized Active Ethiopian Banking App Packages
    target_apps = {
        "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking", 
        "Bank of Abyssinia": "com.boa.boaMobileBanking",
        "Dashen Bank": "com.cr2.amolelight"
    }
    
    master_df = pd.DataFrame()
    for bank, app_id in target_apps.items():
        raw_df = scrape_bank_reviews(app_id, bank, count_target=500)
        clean_df = preprocess_data(raw_df)
        master_df = pd.concat([master_df, clean_df], ignore_index=True)
    
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/cleaned_reviews.csv"
    master_df.to_csv(output_path, index=False)
    print(f"\n[✓] Pipeline execution finalized. Dataset secured: {output_path}")