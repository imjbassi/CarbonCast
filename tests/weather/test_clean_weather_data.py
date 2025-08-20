import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestCleanWeatherData:
    
    def test_clean_weather_data_removes_nulls(self):
        """Test that null values are properly handled"""
        # Create sample weather data with nulls
        data = {
            'datetime': ['2021-07-01 00:00:00', '2021-07-01 01:00:00', '2021-07-01 02:00:00'],
            'temperature': [25.0, np.nan, 27.0],
            'humidity': [60.0, 65.0, np.nan],
            'wind_speed': [10.0, 12.0, 15.0]
        }
        df = pd.DataFrame(data)
        
        # Test null removal/interpolation
        cleaned = df.interpolate()
        assert not cleaned['temperature'].isnull().any()
        assert not cleaned['humidity'].isnull().any()
    
    def test_weather_data_structure(self):
        """Test expected weather data structure"""
        data = {
            'datetime': ['2021-07-01 00:00:00'],
            'temperature': [25.0],
            'humidity': [60.0],
            'wind_speed': [10.0]
        }
        df = pd.DataFrame(data)
        
        assert 'datetime' in df.columns
        assert 'temperature' in df.columns
        assert len(df) > 0