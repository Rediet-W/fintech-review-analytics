
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    bank_id INT NOT NULL,
    review_text TEXT NOT NULL,
    rating INT NOT NULL CONSTRAINT check_star_rating CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL,
    sentiment_score NUMERIC(5, 4) NOT NULL,
    identified_theme VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    CONSTRAINT fk_bank_relation FOREIGN KEY (bank_id) REFERENCES banks (bank_id) ON DELETE CASCADE
);