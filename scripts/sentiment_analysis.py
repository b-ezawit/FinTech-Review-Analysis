import os
import pandas as pd
from transformers import pipeline

def run_sentiment_analysis():
    # 1. Load the cleaned master dataset from Task 1
    input_path = "data/raw/bank_reviews_cleaned.csv"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Master dataset not found at {input_path}. Please run Task 1 first.")
    
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} reviews for sentiment analysis.")

    # 2. Initialize the Hugging Face sentiment analysis pipeline using DistilBERT
    print("Loading DistilBERT sentiment model...")
    # Note: DistilBERT SST-2 natively outputs POSITIVE / NEGATIVE. We handle neutral mapping or confidence scores.
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    sentiments = []
    scores = []

    print("Analyzing reviews...")
    # Process reviews in batches or one-by-one with truncation for safety (max 512 tokens)
    reviews_list = df['review'].astype(str).tolist()
    
    # Run pipeline in chunks or list comprehension
    for text in reviews_list:
        try:
            # Truncate text to 512 tokens equivalent length safely
            result = sentiment_pipeline(text[:512])[0]
            label = result['label'].lower()  # 'positive' or 'negative'
            score = result['score']
            
            sentiments.append(label)
            scores.append(score)
        except Exception as e:
            sentiments.append("neutral")
            scores.append(0.0)

    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores

    # 3. Aggregate sentiment scores by bank and star rating
    print("\n--- Sentiment Aggregation Summary ---")
    agg_summary = df.groupby(['bank', 'rating']).agg(
        mean_confidence=('sentiment_score', 'mean'),
        total_reviews=('review', 'count')
    ).reset_index()
    print(agg_summary)

    # 4. Save processed output for downstream tasks
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/reviews_with_sentiment.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved sentiment analysis results to {output_path}")

if __name__ == "__main__":
    run_sentiment_analysis()
