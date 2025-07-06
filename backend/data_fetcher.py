import requests
import pandas as pd
from datetime import datetime

class TaiwanStockFetcher:
    def __init__(self):
        self.base_url = "https://www.twse.com.tw/exchangeReport/"
        
    def get_daily_data(self, date):
        """獲取台灣股市每日交易數據"""
        date_str = date.strftime("%Y%m%d")
        url = f"{self.base_url}STOCK_DAY?response=json&date={date_str}&stockNo=2330"
        response = requests.get(url)
        data = response.json()
        
        if data['stat'] == 'OK':
            df = pd.DataFrame(data['data'], columns=data['fields'])
            df['date'] = pd.to_datetime(df['date'])
            return df
        else:
            raise ValueError("Failed to fetch data")
    
    def get_stock_list(self):
        """獲取台灣上市公司列表"""
        url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json"
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data['data'], columns=data['fields'])