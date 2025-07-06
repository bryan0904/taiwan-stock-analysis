import pandas as pd
import numpy as np

class TechnicalAnalysis:
    @staticmethod
    def moving_average(data, window=5):
        """計算移動平均線"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def rsi(data, window=14):
        """計算相對強弱指標(RSI)"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(data, short_window=12, long_window=26, signal_window=9):
        """計算MACD指標"""
        short_ema = data.ewm(span=short_window, adjust=False).mean()
        long_ema = data.ewm(span=long_window, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        return macd_line, signal_line
    
    @staticmethod
    def bollinger_bands(data, window=20, num_std=2):
        """計算布林通道"""
        ma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()
        upper_band = ma + (std * num_std)
        lower_band = ma - (std * num_std)
        return upper_band, ma, lower_band
    
    @staticmethod
    def atr(high, low, close, window=14):
        """計算真實波動幅度(ATR)"""
        tr = pd.DataFrame(index=high.index)
        tr['h-l'] = high - low
        tr['h-pc'] = (high - close.shift(1)).abs()
        tr['l-pc'] = (low - close.shift(1)).abs()
        tr['tr'] = tr.max(axis=1)
        return tr['tr'].rolling(window=window).mean()