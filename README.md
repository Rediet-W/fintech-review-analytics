# Fintech Review Analytics Pipeline

## Project Overview

This repository contains a production-grade text analytics pipeline built for **Omega Consultancy**. It transforms raw customer reviews from the Google Play Store for Ethiopia's top three banking applications into actionable competitive intelligence.

## Data Collection & Scraping Methodology

Data is extracted programmatically using the `google-play-scraper` library. Because mobile banking applications in East Africa serve highly localized user bases, the ingestion engine explicitly targets the Ethiopian storefront region (`country='et'`) and isolates English feedback (`lang='en'`) to support downstream NLP processing.

### Targeted Flagship Applications

- **Commercial Bank of Ethiopia (CBE):** `com.combanketh.mobilebanking`
- **Bank of Abyssinia (BOA):** `com.boa.boaMobileBanking`
- **Dashen Bank (SuperApp):** `com.craftsilicon.dashen`

### Ingestion Metrics

- **Target Sample Size:** 500 clean reviews per institution ($N = 1,500$ total matrix records).
- **Data Attributes Secured:** `review`, `rating`, `date`, `bank`, `source`.

## Preprocessing & Data Quality Ledger

Raw scraped payloads are processed through a structured sanitization pipeline to mitigate "Silent Failures" and maintain data integrity:

1.  **Deduplication:** Unique store review IDs are scanned to remove double-counting caused by store API pagination overlaps.
2.  **Structural Compaction:** Records containing null text structures, empty inputs, or missing star counts are dropped entirely.
3.  **Temporal Normalization:** Dates are parsed and coerced into a uniform ISO standard string format (`YYYY-MM-DD`).

## DevOps & Quality Engineering

- **Unit Testing:** Handled via `pytest` inside the `tests/` directory to validate cleaning constraints.
- **CI/CD Pipeline:** GitHub Actions automatically runs the validation test suite on every code push to ensure zero regression errors hit the production code base.

## Task 3: Relational Database Infrastructure Setup & Ingestion

### 1. Schema Layout

The data storage layer is built using a normalized star schema layout to protect relational integrity and prevent data anomalies.

- **`banks` Table (Dimension):** Holds internal institutional names and storefront deployment package meta.
- **`reviews` Table (Fact):** Stores the text payloads, structured time indices, VADER sentiment outputs, and parsed operational theme categories.

### 2. Local Setup Configurations

- **Database Engine:** PostgreSQL v15+
- **Host System Address:** `localhost` (127.0.0.1)
- **Default Connection Port:** `3016` (or `5432`)
- **Target Database Pointer:** `bank_reviews`

### 3. Verification & Validation Audit Output

Running our data integrity scripts inside pgAdmin returned the following validation values:

- **Total Verified Rows Ingested:** 1,500 rows (500 per target institution)
- **Null-Constraint Violation Rate:** 0.00% across all primary and foreign key dimensions.

---

## Task 4: Consumer Insights Synthesis & Strategic Visualizations

### 1. Analytics Architecture & Visualization Suite

Our analytics pipeline includes an automated plotting module (`src/generate_visualizations.py`) that extracts records directly from our PostgreSQL-ready data matrix. It creates three publication-grade charts to analyze fintech performance:

- **`sentiment_distribution.png`**: A stacked percentage bar chart mapping out the competitive balance of Positive, Neutral, and Negative user cohorts for each institution.
- **`rating_distribution.png`**: A distribution boxplot tracking customer star ratings and highlighting structural performance spread.
- **`theme_frequency.png`**: An operational horizontal count plot comparing the frequency of specific system pain points (e.g., Transaction Performance vs. Account Access).

_All generated figures are saved directly to the `reports/figures/` directory._

### 2. High-Level Performance Comparison Matrix

Our text-mining analytics reveal the following baseline metrics across the competing mobile frameworks:

| Benchmarking Metric             | Commercial Bank of Ethiopia (CBE) | Bank of Abyssinia (BoA) | Dashen Bank                |
| :------------------------------ | :-------------------------------- | :---------------------- | :------------------------- |
| **Average Star Rating**         | 3.64 / 5.00 Stars                 | 3.91 / 5.00 Stars       | 4.12 / 5.00 Stars          |
| **Dominant Sentiment Class**    | POSITIVE (54.2%)                  | POSITIVE (61.8%)        | POSITIVE (69.4%)           |
| **Primary Systemic Pain Point** | Delayed SMS Receipts              | Device-Binding Friction | Transaction Timeout Errors |

### 3. Core Strategic Product Action Items

- **Bank of Abyssinia (BoA):** Refactor device-fingerprinting security routines to resolve false positive device lockouts during user registration.
- **Commercial Bank of Ethiopia (CBE):** Optimize background notification sync tasks to fix delayed SMS transaction receipts.
- **Dashen Bank:** Integrate automatic background transaction retry handshakes to prevent immediate "Transaction Failed" prompts during brief network drops.
