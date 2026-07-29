import os
import pandas as pd
from google_play_scraper import reviews, Sort

# Define app details for the three banks
BANKS = {
    "Commercial Bank of Ethiopia": {
        "package": "com.combanketh.mobilebanking",
        "filename": "cbe_reviews.csv"
    },
    "Bank of Abyssinia": {
        "package": "com.boa.boaMobileBanking",
        "filename": "boa_reviews.csv"
    },
    "Dashen Bank": {
        "package": "com.cr2.amolelight",
        "filename": "dashen_reviews.csv"
    }
}

TARGET_REVIEWS_PER_BANK = 400

def preprocess_data(raw_data, bank_name):
    df = pd.DataFrame(raw_data)
    if df.empty:
        print(f"No reviews found for {bank_name}.")
        return pd.DataFrame(columns=['review', 'rating', 'date', 'bank', 'source'])
    
    # Map fields to required schema
    formatted_data = []
    for _, r in df.iterrows():
        formatted_data.append({
            "review": r.get('content'),
            "rating": r.get('score'),
            "date": r.get('at').strftime('%Y-%m-%d') if pd.notnull(r.get('at')) else None,
            "bank": bank_name,
            "source": "Google Play"
        })
    
    clean_df = pd.DataFrame(formatted_data)
    initial_count = len(clean_df)
    
    # 1. Drop rows missing review text or rating
    clean_df = clean_df.dropna(subset=['review', 'rating'])
    
    # 2. Remove duplicate reviews based on text content
    clean_df = clean_df.drop_duplicates(subset=['review'])
    
    # 3. Ensure date format
    clean_df['date'] = pd.to_datetime(clean_df['date']).dt.strftime('%Y-%m-%d')
    
    print(f"[{bank_name}] Cleaned rows: {len(clean_df)} (Dropped {initial_count - len(clean_df)} invalid/duplicates).")
    return clean_df

def main():
    os.makedirs("data/raw", exist_ok=True)
    all_dfs = []

    for bank_name, info in BANKS.items():
        print(f"Scraping reviews for {bank_name} ({info['package']})...")
        try:
            result, _ = reviews(
                info['package'],
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=TARGET_REVIEWS_PER_BANK
            )
            
            cleaned_bank_df = preprocess_data(result, bank_name)
            
            # Save individual CSV per bank inside data/raw/
            individual_path = os.path.join("data/raw", info['filename'])
            cleaned_bank_df.to_csv(individual_path, index=False)
            print(f"Saved individual file: {individual_path}")
            
            all_dfs.append(cleaned_bank_df)
            
        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")

    # Combine all into a master dataset as well
    if all_dfs:
        master_df = pd.concat(all_dfs, ignore_index=True)
        master_path = os.path.join("data/raw", "bank_reviews_cleaned.csv")
        master_df.to_csv(master_path, index=False)
        print(f"Saved combined master dataset: {master_path} (Total records: {len(master_df)})")

if __name__ == "__main__":
    main()

