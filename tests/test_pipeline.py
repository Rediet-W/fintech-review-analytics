import pytest
import pandas as pd
from src.data_collection import preprocess_data

def test_preprocessing_cleansing_logic():
    """
    Validates that our data strategy treats duplicates, missing data,
    handles date normalization, and outputs exactly the 5 required columns.
    """
    # Create mock dirty dataframe mapping out real-world faults
    # We still use 'review_id' here because preprocess_data needs it to drop duplicates
    dirty_mock_data = pd.DataFrame({
        'review_id': ['REV1', 'REV1', 'REV2', 'REV3', 'REV4'], # Contains duplicate ID
        'review_text': ['Excellent App', 'Excellent App', None, '   ', 'Buggy transfer system'], # Contains nulls & whitespace fields
        'rating': [5, 5, 1, 2, 1],
        'date': [pd.Timestamp('2026-05-13 10:30:00'), pd.Timestamp('2026-05-13 10:30:00'), pd.Timestamp('2026-05-14'), pd.Timestamp('2026-05-15'), pd.Timestamp('2026-05-16')],
        'bank': ['Dashen Bank', 'Dashen Bank', 'Commercial Bank of Ethiopia', 'Bank of Abyssinia', 'Commercial Bank of Ethiopia'],
        'source': ['Google Play'] * 5
    })
    
    cleaned_df = preprocess_data(dirty_mock_data)
    
    # 1. Structural Assertions
    assert len(cleaned_df) == 2, "Pipeline must drop duplicates and incomplete text rows safely."
    
    # 2. Check strict column layout constraints
    expected_columns = ['review', 'rating', 'date', 'bank', 'source']
    assert list(cleaned_df.columns) == expected_columns, f"Output columns must match exactly: {expected_columns}"
    
    # 3. Content Assertions (Verifying that 'review_text' became 'review' and whitespace was stripped)
    assert cleaned_df['review'].iloc[0] == 'Excellent App'
    assert cleaned_df['review'].iloc[1] == 'Buggy transfer system'
    
    # 4. Temporal Normalization Assertion
    assert cleaned_df['date'].iloc[0] == '2026-05-13', "Dates must match uniform YYYY-MM-DD string syntax."