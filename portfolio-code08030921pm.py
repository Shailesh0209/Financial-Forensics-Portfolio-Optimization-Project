import pandas as pd
import numpy as np

# Load Datasets
def load_data(prefix):
    df_annual_pl_1 = pd.read_csv(f"{prefix}/Annual_P_L_1.csv")
    df_annual_pl_2 = pd.read_csv(f"{prefix}/Annual_P_L_2.csv")
    df_balance_sheet = pd.read_csv(f"{prefix}/Balance_Sheet.csv")
    df_cash_flow = pd.read_csv(f"{prefix}/cash_flow_statements.csv")
    df_other_metrics = pd.read_csv(f"{prefix}/other_metrics.csv")
    df_ratios_1 = pd.read_csv(f"{prefix}/ratios_1.csv")
    df_ratios_2 = pd.read_csv(f"{prefix}/ratios_2.csv")
    df_price = pd.read_csv(f"{prefix}/price.csv")

    dfs = [df_annual_pl_1, df_annual_pl_2, df_balance_sheet, df_cash_flow,
           df_other_metrics, df_ratios_1, df_ratios_2, df_price]

    data = dfs[0]
    for df in dfs[1:]:
        data = data.merge(df, on=['BSE Code', 'NSE Code', 'Name', 'Industry', 'Current Price', 'Market Capitalization'], how='left')

    return data

# Load T1 and T2 data
data_T1 = load_data('T1_data')
data_T2 = load_data('T2_data')

# Strategy: Simple Ranking based on ROE, ROCE, and Price Appreciation
data_T1['ROE'] = data_T1['Return on equity'].fillna(0)
data_T1['ROCE'] = data_T1['Return on capital employed'].fillna(0)
data_T2 = data_T2[['BSE Code', 'Current Price']].rename(columns={'Current Price': 'Price_T2'})

# Merge T2 Prices for appreciation calculation
data = data_T1.merge(data_T2, on='BSE Code', how='left')
data['Price_Appreciation'] = (data['Price_T2'] - data['Current Price']) / data['Current Price']

# Rank stocks based on ROE, ROCE, and Price Appreciation
data['Score'] = data[['ROE', 'ROCE', 'Price_Appreciation']].mean(axis=1)
data = data.sort_values(by='Score', ascending=False)

# Portfolio Allocation
budget = 1000000
selected_stocks = []
total_cost = 0

for _, row in data.iterrows():
    price = row['Current Price']
    if total_cost + price <= budget:
        units = np.floor((budget / 10) / price)  # investing evenly across ~10 stocks
        if units <= 0:
            continue
        total_cost += units * price
        selected_stocks.append({
            'BSE Code': row['BSE Code'],
            'NSE Code': row['NSE Code'],
            'Company Name': row['Name'],
            'Units': units
        })

# Prepare Submission Files
portfolio_df = pd.DataFrame(selected_stocks)
score_share_df = pd.DataFrame({
    'Student-ID': ['Student1', 'Student2', 'Student3', 'Student4'],
    'Score_Share': [25, 25, 25, 25]
})

# Save files for submission
portfolio_df.to_csv('team_03_portfolio.csv', index=False)
score_share_df.to_csv('team_03_score_share.csv', index=False)

# Output for checking
print(portfolio_df)
print(score_share_df)

# Save files
print(f'Total Portfolio Cost: INR {total_cost:.2f}')
