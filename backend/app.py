from flask import Flask, jsonify, request
from data_fetcher import TaiwanStockFetcher
from fundamental_analysis import FundamentalAnalysis
from technical_analysis import TechnicalAnalysis
from portfolio_analysis import PortfolioAnalysis
import pandas as pd

app = Flask(__name__)

@app.route('/api/stock/daily', methods=['GET'])
def get_daily_data():
    date_str = request.args.get('date')
    date = datetime.strptime(date_str, '%Y%m%d')
    fetcher = TaiwanStockFetcher()
    data = fetcher.get_daily_data(date)
    return jsonify(data.to_dict('records'))

@app.route('/api/stock/fundamental', methods=['POST'])
def analyze_fundamental():
    data = request.json
    result = {
        'pe_ratio': FundamentalAnalysis.calculate_pe_ratio(data['price'], data['eps']),
        'pb_ratio': FundamentalAnalysis.calculate_pb_ratio(data['price'], data['book_value_per_share']),
        'peg_ratio': FundamentalAnalysis.calculate_peg_ratio(data['pe_ratio'], data['earnings_growth_rate']),
        'dividend_yield': FundamentalAnalysis.calculate_dividend_yield(data['dividend'], data['price']),
        'roe': FundamentalAnalysis.calculate_roe(data['net_income'], data['shareholders_equity']),
        'roa': FundamentalAnalysis.calculate_roa(data['net_income'], data['total_assets']),
        'debt_ratio': FundamentalAnalysis.calculate_debt_ratio(data['total_liabilities'], data['total_assets']),
        'current_ratio': FundamentalAnalysis.calculate_current_ratio(data['current_assets'], data['current_liabilities'])
    }
    return jsonify(result)

@app.route('/api/portfolio/optimize', methods=['POST'])
def optimize_portfolio():
    data = request.json
    returns = pd.Series(data['returns'])
    cov_matrix = pd.DataFrame(data['cov_matrix'])
    
    optimal_weights = PortfolioAnalysis.max_sharpe_ratio_portfolio(returns, cov_matrix)
    
    return jsonify({
        'weights': optimal_weights.tolist(),
        'expected_return': PortfolioAnalysis.portfolio_return(optimal_weights, returns),
        'volatility': PortfolioAnalysis.portfolio_volatility(optimal_weights, cov_matrix),
        'sharpe_ratio': PortfolioAnalysis.sharpe_ratio(optimal_weights, returns, cov_matrix)
    })

if __name__ == '__main__':
    app.run(debug=True)