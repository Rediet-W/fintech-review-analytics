import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_fintech_plots(csv_path: str, output_dir: str):
    print("[*] Loading processed text-mining dataset...")
    if not os.path.exists(csv_path):
        print(f"[X] Source metrics file not found at: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Apply standard clean styling parameters
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'figure.titlesize': 16
    })
    
    # ----------------------------------------------------
    # PLOT 1: Stacked Sentiment Distribution Percentage Chart
    # ----------------------------------------------------
    print("[*] Generating Plot 1: Stacked Sentiment Proportions...")
    plt.figure(figsize=(10, 6))
    sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
    sentiment_pct = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100
    
    # Use distinct accessible color palettes
    sentiment_pct.plot(kind='bar', stacked=True, color=['#e74c3c', '#95a5a6', '#2ecc71'], ax=plt.gca())
    plt.title('Comparative Sentiment Profile Across Ethiopian Fintech Apps')
    plt.xlabel('Banking Institution')
    plt.ylabel('Proportion Percentage (%)')
    plt.xticks(rotation=0)
    plt.legend(title='Sentiment Metric')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sentiment_distribution.png'), dpi=300)
    plt.close()
    
    # ----------------------------------------------------
    # PLOT 2: Customer Rating Boxplot and Distribution Spread
    # ----------------------------------------------------
    print("[*] Generating Plot 2: App Rating Density Variations...")
    plt.figure(figsize=(9, 6))
    sns.boxplot(x='bank', y='rating', data=df, palette='Set2', width=0.4)
    plt.title('Star Rating Variance and Dispersion by Platform')
    plt.xlabel('Banking Institution')
    plt.ylabel('Star Metric Distribution (1-5 Stars)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rating_distribution.png'), dpi=300)
    plt.close()
    
    # ----------------------------------------------------
    # PLOT 3: Operational Theme Frequency Chart (Excluding General Feedback)
    # ----------------------------------------------------
    print("[*] Generating Plot 3: Functional Domain Frequency...")
    plt.figure(figsize=(11, 6))
    operational_df = df[df['identified_theme'] != 'General Feedback']
    
    sns.countplot(
        y='identified_theme', 
        hue='bank', 
        data=operational_df, 
        palette='viridis',
        order=operational_df['identified_theme'].value_counts().index
    )
    plt.title('Volume Comparison of Core Operational Pain Points & Drivers')
    plt.xlabel('Absolute Count of Customer Reviews')
    plt.ylabel('Identified Functional Domains')
    plt.legend(title='Institution', loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'theme_frequency.png'), dpi=300)
    plt.close()
    
    print(f"[✓] Visualization suite successfully saved to folder: {output_dir}")

if __name__ == "__main__":
    generate_fintech_plots("data/raw/sentiment_reviews.csv", "reports/figures")