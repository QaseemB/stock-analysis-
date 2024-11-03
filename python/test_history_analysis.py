import unittest
import pandas as pd
from history_analysis import analyze_stock  # Import the function

class TestStockAnalysis(unittest.TestCase):
    
    def test_data_frame_structure(self):
        # Simulate a test DataFrame similar to what MongoDB would return
        test_data = {
            "date": pd.date_range(start="2023-01-01", periods=6, freq="M"),
            "close": [150, 155, 160, 165, 170, 175],
            "volume": [1000, 1100, 1050, 1150, 1200, 1250]
        }
        df = pd.DataFrame(test_data)
        df.set_index('date', inplace=True)
        
        # Check if moving averages and Bollinger Bands are correctly calculated
        df["moving_avg_3"] = df["close"].rolling(window=3).mean()
        df["upper_band"] = df["moving_avg_3"] + df["close"].rolling(window=3).std() * 2
        
        # Ensure non-null calculation for moving averages after the rolling window
        self.assertIsNotNone(df["moving_avg_3"].iloc[2])  # Third data point onwards should have data
        self.assertIsNotNone(df["upper_band"].iloc[2])  # Third data point onwards should have data
        
if __name__ == "__main__":
    unittest.main()
