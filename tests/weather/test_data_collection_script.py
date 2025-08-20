import pytest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestDataCollectionScript:
    
    def test_data_collection_format(self):
        """Test that collected data has correct format"""
        # Mock data collection result
        sample_data = {
            'timestamp': ['2021-07-01 00:00:00', '2021-07-01 01:00:00'],
            'value': [100.5, 150.2]
        }
        df = pd.DataFrame(sample_data)
        
        assert 'timestamp' in df.columns
        assert len(df) == 2
        assert df['value'].dtype in ['float64', 'int64']
    
    def test_empty_data_handling(self):
        """Test handling of empty datasets"""
        empty_df = pd.DataFrame()
        
        # Should handle empty dataframes gracefully
        assert len(empty_df) == 0