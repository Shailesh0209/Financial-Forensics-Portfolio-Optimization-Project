import pandas as pd
import numpy as np
import cvxpy as cp
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

# Load required datasets
t1_pnl_1 = load_data('T1_data/Annual_P_L_1.csv')
t2_pnl_1 = load_data('T2_data/Annual_P_L_1.csv')
t1_price = load_data('T1_data/price.csv')
t2_price = load_data('T2_data/price.csv')

def mean_variance_optimization(expected_returns: np.ndarray, covariance_matrix: np.ndarray) -> np.ndarray:
    num_assets = len(expected_returns)
    weights = cp.Variable(num_assets)
    portfolio_variance = cp.quad_form(weights, covariance_matrix)
    portfolio_return = expected_returns @ weights

    constraints = [
        cp.sum(weights) == 1,
        weights >= 0,          # Allow assets with no allocation (0% allocation)
        weights <= 0.10,       # Max 10% to avoid over-concentration
        portfolio_return >= 0
    ]

    # Emphasize returns more than variance for higher score
    objective = cp.Maximize(portfolio_return - 0.1 * portfolio_variance)

    problem = cp.Problem(objective, constraints)

    try:
        problem.solve(solver=cp.SCS, verbose=False)
    except cp.error.SolverError:
        problem.solve()

    if weights.value is None:
        raise ValueError("Optimization failed: No feasible solution found.")

    optimized_weights = np.clip(weights.value, 0, None)
    optimized_weights /= optimized_weights.sum()

    return optimized_weights



def calculate_optimized_portfolio_performance(weights: np.ndarray, 
                                              t1_price: pd.DataFrame, 
                                              t2_price: pd.DataFrame, 
                                              total_budget: float) -> Dict:
    # Clip negative weights to zero and normalize again
    weights = np.clip(weights, 0, None)
    weights /= weights.sum()

    # Allocate exact budget by calculating units per asset (integer units)
    asset_prices_t1 = t1_price['Current Price'].values
    asset_prices_t2 = t2_price['Current Price'].values
    
    # Calculate initial units (floor to ensure budget compliance)
    budget_per_asset = weights * total_budget
    units_per_stock = np.floor(budget_per_asset / asset_prices_t1)

    # Recalculate actual total cost (guaranteed not to exceed budget)
    total_cost = np.sum(units_per_stock * asset_prices_t1)
    
    # Recalculate final value based on units bought
    final_value = np.sum(units_per_stock * asset_prices_t2)
    
    portfolio_delta = final_value - total_cost
    percentage_gain_loss = (portfolio_delta / total_cost) * 100
    
    return {
        'total_cost': total_cost,
        'final_value': final_value,
        'portfolio_delta': portfolio_delta,
        'percentage_gain_loss': percentage_gain_loss
    }

def select_optimal_portfolio(t1_price: pd.DataFrame, optimized_weights: np.ndarray, budget: float) -> pd.DataFrame:
    asset_prices = t1_price['Current Price'].values
    stock_names = t1_price['Name'].values
    bse_codes = t1_price.get('BSE Code', pd.Series(['']*len(t1_price))).values
    nse_codes = t1_price.get('NSE Code', pd.Series(['']*len(t1_price))).values
    
    allocated_budget = optimized_weights * budget
    units_per_stock = np.floor(allocated_budget / asset_prices).astype(int)

    selected_stocks = []
    for bse, nse, name, units in zip(bse_codes, nse_codes, stock_names, units_per_stock):
        if units >= 10:  # Only include stocks with at least 10 units
            selected_stocks.append({
                'BSE Code': bse,
                'NSE Code': nse,
                'Name': name,
                'Units': units
            })

    return pd.DataFrame(selected_stocks)



def calculate_final_score(portfolio_performance: Dict, base_score: float = 70, presentation_score: float = 80) -> float:
    pps = base_score + portfolio_performance['percentage_gain_loss']
    pps = min(100, max(0, pps))
    A = 0.5 * pps + 0.5 * presentation_score
    final_score = 0.5 * A + A * 0.5  # Simplified calculation
    return final_score

def generate_csv_files(selected_stocks: pd.DataFrame, score_share: List[Dict], team_id: str):
    selected_stocks.to_csv(f"{team_id}_portfolio.csv", index=False)
    pd.DataFrame(score_share).to_csv(f"{team_id}_score_share.csv", index=False)

def main():
    global t1_price, t2_price

    # Load and merge the price data with missing BSE and NSE codes
    merged_prices = pd.merge(t1_price, t2_price[['Name', 'Current Price']], on='Name', suffixes=('_t1', '_t2')).dropna()

    # Load the price data with codes
    price_data = load_data('T1_data/price.csv')

    # Merge the price_data with the t1_price (and t2_price if necessary) to fill missing codes
    t1_price = pd.merge(merged_prices, price_data[['Name', 'BSE Code', 'NSE Code']], on='Name', how='left')
    t2_price = pd.merge(merged_prices, price_data[['Name', 'BSE Code', 'NSE Code']], on='Name', how='left')

    # Rename columns to avoid conflicts
    t1_price = t1_price.rename(columns={
        'Current Price_t1': 'Current Price',
        'BSE Code_x': 'BSE Code',
        'NSE Code_x': 'NSE Code'
    })
    t2_price = t2_price.rename(columns={
        'Current Price_t2': 'Current Price',
        'BSE Code_y': 'BSE Code',
        'NSE Code_y': 'NSE Code'
    })

    # Ensure the columns are correctly named
    print("Columns in t1_price after renaming:", t1_price.columns)

    # Proceed with your calculations
    positive_stocks = t1_price[t1_price['Return over 3months'] > 0].copy()
    if positive_stocks.empty:
        raise ValueError("No assets with positive returns available.")

    expected_returns = positive_stocks['Return over 3months'].values.astype(np.float64)

    # Improved covariance estimation (if historical data available)
    covariance_matrix = np.diag(np.full(len(expected_returns), 0.0025))

    optimized_weights = mean_variance_optimization(expected_returns, covariance_matrix)

    total_budget = 1_000_000
    portfolio_performance = calculate_optimized_portfolio_performance(
        optimized_weights, positive_stocks, 
        t2_price.loc[positive_stocks.index], total_budget)

    final_score = calculate_final_score(portfolio_performance, presentation_score=80)

    selected_stocks = select_optimal_portfolio(positive_stocks, optimized_weights, budget=total_budget)
    selected_stocks.to_csv('optimal_portfolio.csv', index=False)

    score_share = [
        {'Student-ID': '21F1004597', 'Score_Share': 25},
        {'Student-ID': '21f1005287', 'Score_Share': 25},
        {'Student-ID': '22f1001553', 'Score_Share': 25},
        {'Student-ID': '22f3003192', 'Score_Share': 25}
    ]

    generate_csv_files(selected_stocks, score_share, team_id="team_03")

    # Output results
    print("Portfolio Performance:", portfolio_performance)
    print("Optimized Weights:", optimized_weights)
    print("Final Score:", final_score)

if __name__ == "__main__":
    main()