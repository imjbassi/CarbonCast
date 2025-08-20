import pytest
import os
import json
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_manager import Config

class TestConfigManager:
    
    def test_config_manager_default(self):
        """Test config manager with default settings"""
        config = Config()
        assert config.base_path is not None
        assert config.data_path is not None
    
    def test_config_manager_with_file(self, tmp_path):
        """Test config manager with configuration file"""
        config_content = '{"data_path": "test_data"}'
        config_file = tmp_path / "test_config.json"
        config_file.write_text(config_content)
        
        config = Config(str(config_file))
        assert "test_data" in config.data_path
    
    def test_config_manager_invalid_json(self, tmp_path):
        """Test config manager with invalid JSON"""
        config_file = tmp_path / "invalid_config.json"
        config_file.write_text("invalid json content")
        
        # Should handle invalid JSON gracefully
        config = Config(str(config_file))
        assert config.base_path is not None
    
    def test_config_manager_missing_file(self):
        """Test config manager with missing file"""
        # Should handle missing file gracefully
        config = Config("non_existent_config.json")
        assert config.base_path is not None
    
    def test_get_regions(self):
        """Test getting available regions"""
        config = Config()
        regions = config.get_regions()
        # Should return a list (might be empty if no data directory)
        assert isinstance(regions, list)
    
    def test_validate_region(self):
        """Test region validation"""
        config = Config()
        # Test with obviously invalid region
        assert not config.validate_region("INVALID_REGION_XYZ")
    
    def test_get_config_value(self, tmp_path):
        """Test getting configuration values"""
        config_content = '{"test_key": "test_value", "number_key": 42}'
        config_file = tmp_path / "test_config.json"
        config_file.write_text(config_content)
        
        config = Config(str(config_file))
        assert config.get_config_value("test_key") == "test_value"
        assert config.get_config_value("number_key") == 42
        assert config.get_config_value("missing_key", "default") == "default"
