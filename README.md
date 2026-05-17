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
