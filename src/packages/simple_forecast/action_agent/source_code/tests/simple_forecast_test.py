import unittest
from unittest.mock import patch
import time
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import simple_forecast as sf

class TestTemperatureForecast(unittest.TestCase):
    def setUp(self):
        # Reset global variables before each test
        sf.seconds_to_wait = None
        sf.temperature_history = []
        sf.max_history_length = 5

    def test_on_create_with_seconds(self):
        """Test on_create with seconds_to_wait parameter"""
        result = sf.on_create({"seconds_to_wait": 10})
        self.assertEqual(sf.seconds_to_wait, 10)
        self.assertEqual(result, {})

    def test_on_create_without_seconds(self):
        """Test on_create without seconds_to_wait parameter"""
        result = sf.on_create({})
        self.assertEqual(sf.seconds_to_wait, 0)
        self.assertEqual(result, {})

    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_on_receive_basic(self, mock_sleep):
        """Test basic functionality of on_receive"""
        sf.on_create({"seconds_to_wait": 1})
        result = sf.on_receive({"temperature": 20.0})
        
        self.assertIn("forecasted_temperature", result)
        self.assertIn("elapsed_seconds", result)
        self.assertEqual(result["forecasted_temperature"], 20.0)
        mock_sleep.assert_called_once_with(1)

    @patch('time.sleep')
    def test_on_receive_multiple_temperatures(self, mock_sleep):
        """Test on_receive with multiple temperature inputs"""
        sf.on_create({"seconds_to_wait": 0})
        
        # Send several temperatures
        sf.on_receive({"temperature": 20.0})
        sf.on_receive({"temperature": 22.0})
        result = sf.on_receive({"temperature": 24.0})

        # Expected forecast is average of all temperatures
        expected_forecast = (20.0 + 22.0 + 24.0) / 3
        self.assertEqual(result["forecasted_temperature"], expected_forecast)

    def test_calculate_forecast_max_history(self):
        """Test that _calculate_forecast respects max_history_length"""
        temperatures = [20.0, 22.0, 24.0, 26.0, 28.0, 30.0]  # 6 temperatures
        
        for temp in temperatures:
            sf._calculate_forecast(temp)
        
        # Should only keep last 5 temperatures
        self.assertEqual(len(sf.temperature_history), 5)
        self.assertEqual(sf.temperature_history, temperatures[-5:])

        # Forecast should be average of last 5 temperatures
        actual_forecast = sf._calculate_forecast(32.0)
        self.assertAlmostEqual(actual_forecast, (sum(temperatures[-4:]) + 32.0) / 5)

    def test_calculate_forecast_single_temperature(self):
        """Test _calculate_forecast with a single temperature"""
        forecast = sf._calculate_forecast(20.0)
        self.assertEqual(forecast, 20.0)
        self.assertEqual(len(sf.temperature_history), 1)

    @patch('time.sleep')
    def test_on_receive_float_seconds(self, mock_sleep):
        """Test that on_receive handles float seconds_to_wait"""
        sf.on_create({"seconds_to_wait": "1.5"})
        sf.on_receive({"temperature": 20.0})
        mock_sleep.assert_called_once_with(1)  # Should be converted to int

    def test_on_receive_missing_temperature(self):
        """Test on_receive with missing temperature"""
        sf.on_create({"seconds_to_wait": 0})
        result = sf.on_receive({})
        self.assertEqual(result["forecasted_temperature"], 0)

    def test_temperature_history_persistence(self):
        """Test that temperature history persists between calls"""
        sf.on_create({"seconds_to_wait": 0})
        
        # Add temperatures and verify they're stored
        temperatures = [20.0, 22.0, 24.0]
        for temp in temperatures:
            sf.on_receive({"temperature": temp})
            
        self.assertEqual(sf.temperature_history, temperatures)

if __name__ == '__main__':
    unittest.main()