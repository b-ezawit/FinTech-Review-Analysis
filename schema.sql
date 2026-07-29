-- schema.sql

-- 1. Banks Table (Metadata for the three banks)
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) UNIQUE NOT NULL,
    app_name VARCHAR(255) NOT NULL
);

-- 2. Reviews Table (Stores processed review data linked to banks)
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(50),
    sentiment_score FLOAT,
    identified_theme VARCHAR(100),
    source VARCHAR(100)
);
