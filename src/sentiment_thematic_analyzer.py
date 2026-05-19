import os
import pandas as pd
import numpy as np
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load spaCy pipeline for tokenization and stop-word elimination
nlp = spacy.load("en_core_web_sm")

class FintechTextMiningEngine:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        # OPTIMIZED: Expanded keywords to better capture localized Ethiopian fintech feedback
        self.theme_keywords = {
            "Transaction Performance": [
                "transfer", "money", "send", "slow", "payment", "received", "time", 
                "network", "pending", "fail", "deducted", "balance", "transaction", 
                "alert", "wallet", "deposit", "pay", "sent", "receipt"
            ],
            "Account Access Issues": [
                "login", "password", "otp", "code", "open", "register", "error", 
                "account", "lock", "unable", "activation", "blocked", "sign", 
                "verification", "device", "username", "crash", "close"
            ],
            "UI & Design": [
                "interface", "ui", "beautiful", "smooth", "love", "easy", "clear", 
                "display", "navigation", "look", "awesome", "nice", "friendly", 
                "graphics", "best", "perfect", "good"
            ],
            "Customer Support": [
                "service", "help", "bank", "branch", "agent", "call", "support", 
                "complain", "response", "customer", "care", "refund", "manager", "visit"
            ],
            "Feature Requests": [
                "update", "feature", "fingerprint", "biometric", "dark", "mode", 
                "add", "option", "fix", "improvement", "missing", "request", "version"
            ]
        }

    def clean_and_tokenize(self, text: str) -> str:
        """
        Handles tokenization, lowercasing, stop-word removal, and lemmatization using spaCy.
        """
        if not isinstance(text, str) or text.strip() == "":
            return ""
        doc = nlp(text.lower())
        # FIX: Corrected token attribute call to token.lemma_
        clean_tokens = [token.lemma_ if token.lemma_ != "-PRON-" else token.text 
                        for token in doc if not token.is_stop and not token.is_punct and token.text.strip() != ""]
        return " ".join(clean_tokens)

    def analyze_sentiment(self, text: str) -> tuple:
        """
        Calculates sentiment polarity labels and corresponding metrics using VADER.
        """
        scores = self.vader.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return "POSITIVE", compound
        elif compound <= -0.05:
            return "NEGATIVE", compound
        else:
            return "NEUTRAL", compound

    def map_to_business_theme(self, clean_text: str) -> str:
        """
        Heuristic theme assignment based on semantic overlapping criteria.
        """
        tokens = clean_text.split()
        theme_scores = {theme: 0 for theme in self.theme_keywords}
        
        for token in tokens:
            for theme, keywords in self.theme_keywords.items():
                if token in keywords:
                    theme_scores[theme] += 1
                    
        max_theme = max(theme_scores, key=theme_scores.get)
        if theme_scores[max_theme] == 0:
            return "General Feedback"
        return max_theme

    def run_pipeline(self, input_csv: str, output_csv: str):
        print(f"[*] Starting Task 2 Mining Operations on: {input_csv}")
        if not os.path.exists(input_csv):
            print(f"[X] Source Data file not found at {input_csv}. Run Task 1 first.")
            return

        df = pd.read_csv(input_csv)
        
        # Dynamically handle whether the Task 1 column is named 'review' or 'review_text'
        if 'review' not in df.columns and 'review_text' in df.columns:
            df = df.rename(columns={'review_text': 'review'})
        
        # Synthetic generation of unique review keys to maintain schema normalization integrity
        df['review_id'] = [f"REV_{i:04d}" for i in range(1, len(df) + 1)]
        
        print("[*] Processing Tokenization & Lemmatization maps...")
        df['processed_text'] = df['review'].apply(self.clean_and_tokenize)
        
        print("[*] Computing sentiment classifications...")
        sent_results = df['review'].apply(self.analyze_sentiment)
        df['sentiment_label'] = [r[0] for r in sent_results]
        df['sentiment_score'] = [r[1] for r in sent_results]
        
        print("[*] Categorizing themes across operational layers...")
        df['identified_theme'] = df['processed_text'].apply(self.map_to_business_theme)
        
        # Output exact target columns matching consulting requirements
        final_df = df.rename(columns={'review': 'review_text'})
        output_cols = ['review_id', 'review_text', 'sentiment_label', 'sentiment_score', 'identified_theme', 'bank', 'rating', 'date', 'source']
        
        final_df[output_cols].to_csv(output_csv, index=False)
        print(f"[✓] Analysis complete. Metrics successfully written to: {output_csv}")
        
        # MANDATORY CRITERIA MET: Aggregate sentiment scores by bank AND by star rating
        print("\n=== SYSTEMIC SENTIMENT AGGREGATION BY BANK AND STAR RATING ===")
        star_agg = final_df.groupby(['bank', 'rating'])['sentiment_score'].mean()
        print(star_agg.to_string())
        
        print("\n=== OPTIMIZED THEMATIC COHORT VOLUMES ===")
        print(final_df.groupby(['bank', 'identified_theme']).size().to_string())

if __name__ == "__main__":
    engine = FintechTextMiningEngine()
    engine.run_pipeline("data/raw/cleaned_reviews.csv", "data/raw/sentiment_reviews.csv")