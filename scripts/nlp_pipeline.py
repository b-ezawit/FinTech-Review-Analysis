import os
import pandas as pd
from transformers import pipeline

def load_data():
    """Loads the cleaned reviews dataset from Task 1."""
    input_path = "data/raw/bank_reviews_cleaned.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file not found at {input_path}")
    df = pd.read_csv(input_path)
    # Generate a unique review_id for each row if it doesn't exist
    df['review_id'] = [f"REV_{i+1:04d}" for i in range(len(df))]
    return df

def apply_sentiment_analysis(df):
    """Applies DistilBERT sentiment classification to the reviews."""
    print("Running sentiment analysis pipeline...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    
    sentiments = []
    scores = []
    
    for text in df['review'].astype(str).tolist():
        try:
            result = sentiment_pipeline(text[:512])[0]
            sentiments.append(result['label'].lower())
            scores.append(result['score'])
        except Exception:
            sentiments.append("neutral")
            scores.append(0.0)
            
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    return df

def assign_theme(text):
    """Maps review text to a business theme based on keyword rules."""
    text = str(text).lower()
    if any(k in text for k in ['login', 'otp', 'password', 'sign', 'account', 'pin', 'access']):
        return 'Account Access Issues'
    elif any(k in text for k in ['transfer', 'slow', 'pending', 'fail', 'transaction', 'balance', 'doesn work', 'working']):
        return 'Transaction Performance'
    elif any(k in text for k in ['app', 'application', 'apps', 'update', 'fix', 'ui', 'design', 'version', 'better']):
        return 'UI & Design & App Stability'
    elif any(k in text for k in ['service', 'support', 'call', 'help', 'feature', 'fingerprint', 'boa', 'cbe', 'dashen', 'amole']):
        return 'Customer Support & Bank Specifics'
    else:
        return 'General Feedback'

def apply_thematic_analysis(df):
    """Assigns themes to each review."""
    print("Applying thematic classification...")
    df['identified_theme'] = df['review'].apply(assign_theme)
    return df

def main():
    # 1. Load data
    df = load_data()
    
    # 2. Run sentiment pipeline
    df = apply_sentiment_analysis(df)
    
    # 3. Run thematic pipeline
    df = apply_thematic_analysis(df)
    
    # 4. Format columns to match exact requirements: review_id, review_text, sentiment_label, sentiment_score, identified_theme
    # Rename 'review' column to 'review_text' to match instructions exactly
    df = df.rename(columns={'review': 'review_text'})
    
    final_columns = ['review_id', 'review_text', 'sentiment_label', 'sentiment_score', 'identified_theme']
    output_df = df[final_columns]
    
    # 5. Save results to CSV
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/pipeline_output.csv"
    output_df.to_csv(output_path, index=False)
    print(f"Pipeline complete! Saved processed data to {output_path}")

if __name__ == "__main__":
    main()
