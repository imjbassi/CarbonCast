import os
import json
import sys
from typing import Dict, Any, Optional

class Config:
    """Configuration management for CarbonCast project"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.base_path = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(self.base_path, "data")
        self.config = {}
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str) -> None:
        """Load configuration from JSON file with error handling"""
        try:
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Config file not found: {config_file}")
                
            with open(config_file, 'r') as f:
                self.config = json.load(f)
                
            # Update paths from config
            if 'data_path' in self.config:
                self.data_path = os.path.expanduser(self.config['data_path'])
                if not os.path.isabs(self.data_path):
                    self.data_path = os.path.join(self.base_path, self.data_path)
                    
            print(f"Configuration loaded from {config_file}")
            
        except FileNotFoundError as e:
            print(f"Warning: {e}. Using default configuration.")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {config_file}: {e}")
            print("Using default configuration.")
        except Exception as e:
            print(f"Error loading config {config_file}: {e}")
            print("Using default configuration.")
    
    def get_data_path(self) -> str:
        """Get the data directory path"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data directory not found: {self.data_path}")
        return self.data_path
    
    def get_file_path(self, region: str, file_type: str, test_period: str = "Jul_Dec_2021") -> str:
        """Get file path for given region and file type with error handling"""
        try:
            data_path = self.get_data_path()
            region_path = os.path.join(data_path, region)
            
            if not os.path.exists(region_path):
                raise FileNotFoundError(f"Region directory not found: {region_path}")
            
            file_patterns = {
                'carbon_direct': f"{region}_carbon_direct_{test_period}.csv",
                'carbon_lifecycle': f"{region}_carbon_lifecycle_{test_period}.csv",
                'forecasts': f"{region}_96hr_forecasts_DA.csv",
                'source_forecasts': f"{region}_96hr_source_prod_forecasts_DA_{test_period}.csv",
                'direct_emissions': f"{region}_direct_emissions.csv",
                'lifecycle_emissions': f"{region}_lifecycle_emissions.csv",
                'weather_forecast': f"{region}_weather_forecast.csv"
            }
            
            if file_type not in file_patterns:
                available_types = ', '.join(file_patterns.keys())
                raise ValueError(f"Unknown file type: {file_type}. Available types: {available_types}")
                
            file_path = os.path.join(region_path, file_patterns[file_type])
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            return file_path
            
        except Exception as e:
            print(f"Error getting file path for {region}/{file_type}: {e}")
            raise
    
    def get_regions(self) -> list:
        """Get list of available regions"""
        try:
            data_path = self.get_data_path()
            regions = [d for d in os.listdir(data_path) 
                      if os.path.isdir(os.path.join(data_path, d))]
            return sorted(regions)
        except Exception as e:
            print(f"Error getting regions: {e}")
            return []
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with default fallback"""
        return self.config.get(key, default)
    
    def validate_region(self, region: str) -> bool:
        """Validate if region exists"""
        try:
            data_path = self.get_data_path()
            region_path = os.path.join(data_path, region)
            return os.path.exists(region_path)
        except Exception:
            return False
