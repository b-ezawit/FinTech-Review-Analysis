# Fintech Review Analytics: Customer Experience Analysis for Ethiopian Banking Apps

## Overview

This project analyzes customer reviews from Ethiopian banking mobile applications to uncover user satisfaction drivers, common complaints, and product improvement opportunities.

The project was completed as part of the **10 Academy Artificial Intelligence Mastery Program – Week 2 Challenge**.

The analysis covers three Ethiopian banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The pipeline transforms raw Google Play Store reviews into actionable insights using:

- Web scraping
- Data preprocessing
- Sentiment analysis
- Thematic analysis
- PostgreSQL database engineering
- Data visualization

---

# Business Problem

Customer reviews contain valuable information about application performance, usability, and user expectations. However, this feedback is mostly unstructured and difficult to analyze manually.

This project helps answer:

- What do users like or dislike about Ethiopian banking apps?
- What issues affect customer satisfaction?
- Which features should banks prioritize improving?

---

# Project Workflow

```

Google Play Store Reviews
|
↓
Data Collection
|
↓
Data Cleaning & Preprocessing
|
↓
Sentiment Analysis
|
↓
Theme Extraction
|
↓
PostgreSQL Storage
|
↓
Visualization & Recommendations

```

---

# Technologies Used

## Data Collection
- Python
- google-play-scraper

## Data Analysis
- pandas
- NumPy
- Scikit-learn
- spaCy
- NLTK

## NLP
- DistilBERT Sentiment Analysis Model
- TF-IDF Keyword Extraction

## Database
- PostgreSQL
- psycopg2 / SQLAlchemy

## Visualization
- Matplotlib
- Seaborn

## Testing & Automation
- pytest
- GitHub Actions

---

# Dataset

Reviews were collected from the Google Play Store for:

| Bank | Reviews |
|---|---|
| Commercial Bank of Ethiopia | 400+ |
| Bank of Abyssinia | 400+ |
| Dashen Bank | 400+ |

Collected fields:

- Review text
- Rating
- Review date
- Bank name
- Source platform

---

# Project Structure

```

fintech-review-analytics/

├── data/
│   └── raw/

├── src/
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── sentiment_analysis.py
│   ├── theme_extraction.py
│   └── database.py

├── notebooks/
│   └── analysis.ipynb

├── tests/

├── sql/
│   └── schema.sql

├── requirements.txt

└── README.md

````

---

# Analysis Approach

## Sentiment Analysis

Customer reviews were classified using:

`distilbert-base-uncased-finetuned-sst-2-english`

Each review received:

- Sentiment label
- Confidence score

Categories:

- Positive
- Negative

---

## Thematic Analysis

TF-IDF keyword extraction was used to identify recurring themes:

Main themes:

- General Feedback
- UI & Design & App Stability
- Transaction Performance
- Account Access Issues
- Feature Requests

---

# Key Findings

## Overall Ratings & Market Position

| Bank | Average Rating |
|---|---|
| Dashen Bank | 3.91 |
| CBE | 3.68 |
| BOA | 3.35 |

### Insights

- **Dashen Bank** achieved the highest average rating, showing stronger overall customer satisfaction and reliability.
- **CBE** showed moderate satisfaction with strong adoption but recurring stability issues.
- **BOA** had the lowest rating, influenced by higher negative sentiment.

---

# Sentiment Distribution

| Bank | Positive | Negative |
|---|---|---|
| Dashen Bank | 58.36% | 41.64% |
| CBE | 53.70% | 46.30% |
| BOA | 44.82% | 55.18% |

Key observation:

- Dashen and CBE maintain positive sentiment majority.
- BOA experiences a negative sentiment imbalance, indicating deeper customer frustrations.

---

# Bank-Specific Insights

## Commercial Bank of Ethiopia (CBE)

### Satisfaction Drivers

- Users appreciate app updates and general usability.
- UI & Design & App Stability received **67 positive mentions**.

Example:

> "ok. easly updare"

### Pain Points

- App stability and login issues remain common.
- UI/Stability complaints: **46 mentions**
- Account access complaints: **26 mentions**

Example:

> "The app stops while log in"

### Recommendations

1. Improve authentication and session stability.
2. Create smoother in-app update experiences.

---

## Bank of Abyssinia (BOA)

### Satisfaction Drivers

- Users value general banking functionality.
- General Feedback received **76 positive mentions**.
- Stability received **51 positive mentions**.

Example:

> "thanks You"

### Pain Points

- Transaction performance issues are a major concern.
- UI/Stability complaints: **54 mentions**
- Transaction Performance complaints: **33 mentions**

### Recommendations

1. Optimize transaction processing and backend performance.
2. Introduce better customer support channels for resolving issues.

---

## Dashen Bank

### Satisfaction Drivers

- Strong positive sentiment around usability and functionality.
- UI & Design & Stability: **75 positive mentions**
- General Feedback: **91 positive mentions**

Example:

> "nice done"

### Pain Points

- Account accessibility remains a concern.
- Account Access Issues: **25 mentions**

Example:

> "accessibility for people with visual impairment should be given more consideration"

### Recommendations

1. Improve accessibility using inclusive design practices.
2. Simplify account recovery and authentication flows.

---

# Database Design

PostgreSQL was used to store processed review data.

## Tables

### Banks

Stores banking application information:

- bank_id
- bank_name
- app_name

### Reviews

Stores review analysis results:

- review_id
- bank_id
- review_text
- rating
- review_date
- sentiment_label
- sentiment_score
- identified_theme
- source

---

# Visualizations

The project includes:

- Sentiment distribution comparison
- Rating distribution by bank
- Theme frequency analysis
- Keyword analysis

These visualizations help translate customer feedback into business decisions.

---

# Testing

Unit tests were created to validate:

- Data preprocessing
- Data quality checks
- Database operations

Run tests:

```bash
pytest
````

---

# Limitations

* Google Play Store scraping limitations
* Sentiment model may not fully understand banking-specific terms
* Reviews represent only users who leave feedback
* Limited support for local languages

---

# Future Improvements

Possible extensions:

* Add Amharic sentiment analysis
* Build a real-time review monitoring dashboard
* Deploy analytics API
* Add automated topic modeling
* Create a Streamlit dashboard

---

# Conclusion

This project demonstrates how customer feedback from fintech applications can be transformed into meaningful business insights.

By combining data engineering, NLP, and analytics, the pipeline helps Ethiopian banks understand customer experiences and prioritize improvements that increase user satisfaction.

---


