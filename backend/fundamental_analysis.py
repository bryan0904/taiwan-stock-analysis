import pandas as pd

class FundamentalAnalysis:
    @staticmethod
    def calculate_pe_ratio(price, eps):
        """計算本益比"""
        return price / eps if eps != 0 else float('inf')
    
    @staticmethod
    def calculate_pb_ratio(price, book_value_per_share):
        """計算股價淨值比"""
        return price / book_value_per_share if book_value_per_share != 0 else float('inf')
    
    @staticmethod
    def calculate_peg_ratio(pe_ratio, earnings_growth_rate):
        """計算PEG比率"""
        return pe_ratio / earnings_growth_rate if earnings_growth_rate != 0 else float('inf')
    
    @staticmethod
    def calculate_dividend_yield(dividend, price):
        """計算股息殖利率"""
        return dividend / price if price != 0 else 0
    
    @staticmethod
    def calculate_roe(net_income, shareholders_equity):
        """計算股東權益報酬率"""
        return net_income / shareholders_equity if shareholders_equity != 0 else 0
    
    @staticmethod
    def calculate_roa(net_income, total_assets):
        """計算資產報酬率"""
        return net_income / total_assets if total_assets != 0 else 0
    
    @staticmethod
    def calculate_debt_ratio(total_liabilities, total_assets):
        """計算負債比率"""
        return total_liabilities / total_assets if total_assets != 0 else 0
    
    @staticmethod
    def calculate_current_ratio(current_assets, current_liabilities):
        """計算流動比率"""
        return current_assets / current_liabilities if current_liabilities != 0 else 0