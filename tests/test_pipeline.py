import pytest
import pandas as pd
import numpy as np
from src.data_collection import preprocess_data

def test_preprocessing_cleansing_logic():
    """
    Validates that our data strategy treats duplicates, missing data, 
    and handles date normalization uniformly.
    """
    # Create mock dirty dataframe mapping out real-world faults
    dirty_mock_data = pd.DataFrame({
        'review_id': ['REV1', 'REV1', 'REV2', 'REV3', 'REV4'], # Contains duplicate ID
        'review_text': ['Excellent App', 'Excellent App', None, '   ', 'Buggy transfer system'], # Contains nulls & whitespace fields
        'rating': [5, 5, 1, 2, 1],
        'date': [pd.Timestamp('2026-05-13 10:30:00'), pd.Timestamp('2026-05-13 10:30:00'), pd.Timestamp('2026-05-14'), pd.Timestamp('2026-05-15'), pd.Timestamp('2026-05-16')],
        'bank': ['Dashen Bank', 'Dashen Bank', 'CBE', 'BOA', 'CBE'],
        'source': ['Google Play'] * 5
    })
    
    cleaned_df = preprocess_data(dirty_mock_data)
    
    # Assertions to turn assumptions into guarantees
    assert len(cleaned_df) == 2, "Pipeline must drop duplicates and incomplete text rows safely."
    assert list(cleaned_df['review_id']) == ['REV1', 'REV4'], "Only uncorrupted, unique records must survive."
    assert '-' in cleaned_df['date'].iloc[0], "Dates must be successfully cast into normalized string partitions (YYYY-MM-DD)."