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
