import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from carbonIntensityCalculator import calculateCarbonIntensity, initialize

class TestCarbonIntensityCalculator:
    
    def test_calculate_carbon_intensity_basic(self):
        """Test basic carbon intensity calculation"""
        # Create sample data that matches the real data structure
        data = {
            'Unnamed: 0': [0, 1],
            'UTC time': pd.to_datetime(['2021-07-01 00:00:00', '2021-07-01 01:00:00']),
            'carbon_intensity': [0, 0],  # Existing column that will be replaced
            'coal': [100, 150],
            'gas': [200, 250],
            'solar': [50, 75]
        }
        df = pd.DataFrame(data)
        
        carbon_rates = {"coal": 760, "gas": 370, "solar": 0}
        
        result = calculateCarbonIntensity(df, carbon_rates, 3)
        
        # Check that carbon_intensity_calculated column was added
        assert 'carbon_intensity_calculated' in result.columns
        assert len(result['carbon_intensity_calculated']) == 2
        assert result['carbon_intensity_calculated'][0] > 0
    
    def test_calculate_carbon_intensity_with_zeros(self):
        """Test carbon intensity calculation with zero values"""
        data = {
            'Unnamed: 0': [0, 1],
            'UTC time': pd.to_datetime(['2021-07-01 00:00:00', '2021-07-01 01:00:00']),
            'carbon_intensity': [0, 0],
            'coal': [0, 0],
            'gas': [0, 0],
            'solar': [0, 0]
        }
        df = pd.DataFrame(data)
        
        carbon_rates = {"coal": 760, "gas": 370, "solar": 0}
        
        # This should handle zero values gracefully
        result = calculateCarbonIntensity(df, carbon_rates, 3)
        assert 'carbon_intensity_calculated' in result.columns
        # With all zeros, carbon intensity should be 0
        assert all(ci == 0 for ci in result['carbon_intensity_calculated'])

    @pytest.fixture
    def sample_csv_file(self, tmp_path):
        """Create a temporary CSV file for testing"""
        csv_content = """UTC time,coal,gas,solar
2021-07-01 00:00:00,100,200,50
2021-07-01 01:00:00,150,250,75"""
        
        csv_file = tmp_path / "test_data.csv"
        csv_file.write_text(csv_content)
        return str(csv_file)
    
    def test_initialize_function(self, sample_csv_file):
        """Test the initialize function"""
        result = initialize(sample_csv_file)
        
        assert isinstance(result, pd.DataFrame)
        assert 'UTC time' in result.columns
        assert len(result) == 2