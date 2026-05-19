# src/database_ingestion.py
import os
import psycopg2
import pandas as pd

# Connection parameters
DB_HOST = "localhost"
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASS = "12345678"  # Using your verified password
DB_PORT = "3016"      # Using your verified port

def execute_ingestion_pipeline(csv_path: str):
    print(f"[*] Commencing DB connection handshake to: '{DB_NAME}'")
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME,
            user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor = conn.cursor()
        
        print("[*] Generating structural tables if missing...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(100) UNIQUE NOT NULL,
                app_name VARCHAR(100) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id VARCHAR(50) PRIMARY KEY,
                bank_id INT NOT NULL,
                review_text TEXT NOT NULL,
                rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
                review_date DATE NOT NULL,
                sentiment_label VARCHAR(20) NOT NULL,
                sentiment_score NUMERIC(5, 4) NOT NULL,
                identified_theme VARCHAR(100) NOT NULL,
                source VARCHAR(50) NOT NULL,
                FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE
            );
        """)
        
        if not os.path.exists(csv_path):
            print(f"[X] Execution failed. Source dataset not found at: {csv_path}")
            return
        df = pd.read_csv(csv_path)
        
        print(f"[*] Detected CSV Columns: {list(df.columns)}")
        
        bank_meta = {
            "Commercial Bank of Ethiopia": "CBE Mobile Banking",
            "Bank of Abyssinia": "BoA Mobile Banking",
            "Dashen Bank": "Amole / Dashen SuperApp"
        }
        
        bank_id_map = {}
        print("[*] Syncing entity indices across dimension tables...")
        for name, app in bank_meta.items():
            cursor.execute("""
                INSERT INTO banks (bank_name, app_name) 
                VALUES (%s, %s) 
                ON CONFLICT (bank_name) DO UPDATE SET app_name = EXCLUDED.app_name
                RETURNING bank_id;
            """, (name, app))
            result = cursor.fetchone()
            if result:
                bank_id_map[name] = result[0]
            else:
                cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s;", (name,))
                bank_id_map[name] = cursor.fetchone()[0]
                
        print(f"[*] Ingesting records ({len(df)} entries) into local target database...")
        records_loaded = 0
        
        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (review_id) DO NOTHING;
                """, (
                    str(row['review_id']),
                    bank_id_map[row['bank']],
                    row['review_text'],
                    int(row['rating']),
                    row['date'],
                    row['sentiment_label'],
                    float(row['sentiment_score']),
                    row['identified_theme'],
                    row.get('source', 'Google Play')
                ))
                records_loaded += 1
            except Exception as line_err:
                print(f"[!] Bypassing row index {idx}: {str(line_err)}")
                continue
                
        conn.commit()
        print(f"[✓] Data load complete. Successfully piped {records_loaded} entries to PostgreSQL storage.")
        
        cursor.execute("SELECT COUNT(*) FROM reviews;")
        print(f"[Audit] Total verified rows now residing in bank_reviews DB: {cursor.fetchone()[0]}")
        
        cursor.close()
        conn.close()
    except Exception as connection_err:
        print(f"[X] Critical connection error or setup failure: {str(connection_err)}")

if __name__ == "__main__":
    execute_ingestion_pipeline("data/raw/sentiment_reviews.csv")