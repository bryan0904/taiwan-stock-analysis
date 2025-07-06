import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PortfolioAnalysis:
    @staticmethod
    def portfolio_return(weights, returns):
        """計算投資組合預期報酬"""
        return np.sum(weights * returns)
    
    @staticmethod
    def portfolio_volatility(weights, cov_matrix):
        """計算投資組合風險"""
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    @staticmethod
    def sharpe_ratio(weights, returns, cov_matrix, risk_free_rate=0):
        """計算夏普比率"""
        port_return = PortfolioAnalysis.portfolio_return(weights, returns)
        port_vol = PortfolioAnalysis.portfolio_volatility(weights, cov_matrix)
        return (port_return - risk_free_rate) / port_vol
    
    @staticmethod
    def max_sharpe_ratio_portfolio(returns, cov_matrix, risk_free_rate=0):
        """計算最大夏普比率投資組合"""
        num_assets = len(returns)
        args = (returns, cov_matrix, risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        initial_guess = num_assets * [1. / num_assets,]
        
        result = minimize(lambda w: -PortfolioAnalysis.sharpe_ratio(w, returns, cov_matrix, risk_free_rate),
                         initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x
    
    @staticmethod
    def efficient_frontier(returns, cov_matrix, return_targets):
        """計算效率前緣"""
        num_assets = len(returns)
        efficient_portfolios = []
        
        for target_return in return_targets:
            constraints = ({'type': 'eq', 'fun': lambda x: PortfolioAnalysis.portfolio_return(x, returns) - target_return},
                          {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0, 1) for asset in range(num_assets))
            initial_guess = num_assets * [1. / num_assets,]
            
            result = minimize(PortfolioAnalysis.portfolio_volatility, initial_guess,
                             args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                efficient_portfolios.append({
                    'return': target_return,
                    'volatility': result.fun,
                    'weights': result.x
                })
        
        return efficient_portfolios
    
    @staticmethod
    def calculate_beta(stock_returns, market_returns):
        """計算Beta係數"""
        covariance = np.cov(stock_returns, market_returns)[0][1]
        variance = np.var(market_returns)
        return covariance / variance
    
    @staticmethod
    def calculate_var(returns, confidence_level=0.95):
        """計算風險值(VaR)"""
        return np.percentile(returns, 100 * (1 - confidence_level))
    
    @staticmethod
    def calculate_max_drawdown(returns):
        """計算最大回撤"""
        cumulative = (1 + returns).cumprod()
        peak = cumulative.expanding(min_periods=1).max()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()
    
    @staticmethod
    def calculate_downside_deviation(returns, mar=0):
        """計算下跌標準差"""
        downside = returns[returns < mar] - mar
        return np.sqrt(np.mean(downside**2))