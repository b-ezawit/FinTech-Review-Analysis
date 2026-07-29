import os
import psycopg2
import pandas as pd

# Database connection configuration matching Docker settings
DB_CONFIG = {
    "dbname": "bank_reviews",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5433"
}

def load_data_to_db():
    csv_path = "data/processed/pipeline_output.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Processed file not found at {csv_path}. Run Task 2 pipeline first.")
    
    df = pd.read_csv(csv_path)
    
    print("Connecting to PostgreSQL Docker container...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # 1. Insert Bank Metadata
        banks_data = [
            ("Commercial Bank of Ethiopia", "Commercial Bank of Ethiopia Mobile"),
            ("Bank of Abyssinia", "Bank of Abyssinia Mobile Banking"),
            ("Dashen Bank", "Dashen Bank Mobile Banking")
        ]
        
        cur.executemany("""
            INSERT INTO banks (bank_name, app_name) 
            VALUES (%s, %s)
            ON CONFLICT (bank_name) DO NOTHING;
        """, banks_data)
        conn.commit()
        print("Inserted bank metadata.")

        # Fetch bank_id mapping directly from database
        cur.execute("SELECT bank_name, bank_id FROM banks;")
        bank_map = {row[0]: row[1] for row in cur.fetchall()}

        # 2. Insert Reviews Data using pipeline output directly
        print("Inserting review records into PostgreSQL...")
        inserted_count = 0

        for _, row in df.iterrows():
            bank_id = bank_map.get(row['bank'])
            if not bank_id:
                continue
                
            cur.execute("""
                INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO NOTHING;
            """, (
                row['review_id'],
                bank_id,
                row['review_text'],
                int(row['rating']),
                row['review_date'],
                row['sentiment_label'],
                float(row['sentiment_score']),
                row['identified_theme'],
                "Google Play"
            ))
            inserted_count += 1

        conn.commit()
        print(f"Successfully inserted {inserted_count} reviews into PostgreSQL!")

        # 3. Run Data Integrity Verification Queries
        print("\n--- Data Integrity Verification ---")
        
        cur.execute("""
            SELECT b.bank_name, COUNT(r.review_id) AS total_reviews
            FROM banks b LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name;
        """)
        print("Reviews per bank:", cur.fetchall())

        cur.execute("""
            SELECT b.bank_name, ROUND(CAST(AVG(r.rating) AS NUMERIC), 2) AS avg_rating
            FROM banks b LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name;
        """)
        print("Average rating per bank:", cur.fetchall())

    except Exception as e:
        conn.rollback()
        print(f"Database insertion error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_data_to_db()
