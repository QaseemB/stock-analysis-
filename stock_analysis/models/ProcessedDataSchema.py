from pymongo import MongoClient
from stock_analysis.config.settings import config
from pydantic import BaseModel, Field
from datetime import date,datetime
from typing import Optional, List

client = MongoClient(config['ATLASURI'])

db = client[config['DB_NAME']]
collection = db[config['DB_PROCESSED_COLLECTION']]

 
class AnalysisSchema(BaseModel):
    date: datetime
    open: float = Field(..., description="The opening price of the stock.")
    high: float = Field(..., description="The highest price of the stock.")
    low: float = Field(..., description="The lowest price of the stock.")
    close: float = Field(..., description="The closing price of the stock.")
    volume: float = Field(..., description="The trading volume of the stock.")
    moving_avg_3: Optional[float] = Field(None, description="The 3-period moving average.")
    moving_avg_6: Optional[float] = Field(None, description="The 6-period moving average.")
    moving_avg_12: Optional[float] = Field(None, description="The 12-period moving average.")
    upper_band: Optional[float] = Field(None, description="The upper Bollinger Band value.")
    lower_band: Optional[float] = Field(None, description="The lower Bollinger Band value.")
    monthly_return: float = Field(..., description="The monthly return percentage.")
    rolling_mean: float = Field(..., description="The rolling mean value.")
    rolling_std: float = Field(..., description="The rolling standard deviation value.")
    ema12: Optional[float] = Field(None, description="The 12-period Exponential Moving Average.")
    ema26: Optional[float] = Field(None, description="The 26-period Exponential Moving Average.")
    macd: Optional[float] = Field(None, description="The Moving Average Convergence Divergence (MACD) value.")
    signal_line: Optional[float] = Field(None, description="The MACD signal line value.")


class ProcessedDataSchema(BaseModel):
    symbol: str = Field(..., description="The stock or asset symbol.")
    latestRefresh: datetime = Field(default_factory= datetime.now, description="The date and time of the latest refresh.")
    analysis: List[AnalysisSchema] = Field(..., description="A list of analysis records for different dates.")