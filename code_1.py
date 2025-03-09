import pandas as pd
import numpy as np # type: ignore

# Load Data
def load_data(path_prefix):
    data = {}
    filenames = ['Annual_P_L_1.csv', 'Annual_P_L_2.csv', 'Balance_Sheet.csv', 'cash_flow_statements.csv',
                 'other_metrics.csv', 'price.csv', 'Quarter_P_L_1.csv', 'Quarter_P_L_2.csv', 'ratios_1.csv', 'ratios_2.csv']
    for file in filenames:
        data[file.split('.')[0]] = pd.read_csv(f'{path_prefix}/{file}')
    return data

# Load T1 and T2 data
data_T1 = load_data('T1_data')
data_T2 = load_data('T2_data')

# Merge relevant datasets on 'BSE Code'
def merge_datasets(data):
    df = data['Annual_P_L_1'].merge(data['Balance_Sheet'], on=['BSE Code', 'Name', 'Industry', 'NSE Code', 'Current Price'], suffixes=('', '_bs'))
    df = df.merge(data['cash_flow_statements'], on=['BSE Code', 'Name', 'Industry', 'NSE Code', 'Current Price'], suffixes=('', '_cf'))
    df = df.merge(data['other_metrics'], on=['BSE Code', 'Name', 'Industry', 'NSE Code', 'Current Price'], suffixes=('', '_om'))
    df = df.merge(data['ratios_1'], on=['BSE Code', 'Name', 'Industry', 'NSE Code', 'Current Price'], suffixes=('', '_r1'))
    df = df.merge(data['price'], on=['BSE Code', 'Name', 'Industry', 'NSE Code', 'Current Price'], suffixes=('', '_pr'))
    return df

# Merged Data for T1 and T2
merged_T1 = merge_datasets(data_T1)
merged_T2 = merge_datasets(data_T2)

# Calculate additional metrics
def compute_metrics(df1, df2):
    combined_df = df1[['BSE Code', 'Name', 'Industry', 'Current Price']].copy()
    combined_df['Price_T1'] = df1['Current Price']
    combined_df['Price_T2'] = df2['Current Price']
    combined_df['Price_change_pct'] = ((combined_df['Price_T2'] - combined_df['Price_T1']) / combined_df['Price_T1']) * 100

    # Example metric: ROE, Current Ratio, Debt to Equity
    combined_df['ROE'] = df1['Return on equity']
    combined_df['Current_Ratio'] = df1['Current ratio']
    combined_df['Debt_Equity'] = df1['Debt to equity']

    # Clean infinite and NaN values
    combined_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    combined_df.dropna(inplace=True)

    return combined_df

metrics_df = compute_metrics(merged_T1, merged_T2)

# Simple strategy: Select Top 10 stocks based on combined ranking of ROE and Price_change_pct
metrics_df['ROE_rank'] = metrics_df['ROE'].rank(ascending=False)
metrics_df['Price_change_rank'] = metrics_df['Price_change_pct'].rank(ascending=False)

# Combined ranking (simple addition of ranks)
metrics_df['combined_rank'] = metrics_df['ROE_rank'] + metrics_df['Price_change_rank']
portfolio_df = metrics_df.sort_values('combined_rank').head(10)

# Allocate portfolio based on equal weight
budget = 1000000  # INR 10,00,000
equal_investment = budget / len(portfolio_df)
portfolio_df['Units'] = (equal_investment / portfolio_df['Price_T1']).astype(int)
portfolio_df['Investment'] = portfolio_df['Units'] * portfolio_df['Price_T1']

# Portfolio summary
portfolio_summary = portfolio_df[['BSE Code', 'Name', 'Units', 'Price_T1', 'Investment']]
total_investment = portfolio_summary['Investment'].sum()

# Ensure total investment is within budget
assert total_investment <= budget

# Export Portfolio to CSV
portfolio_summary.to_csv('final_portfolio.csv', index=False)

# Backtesting portfolio performance
portfolio_df['Portfolio_Value_T2'] = portfolio_df['Units'] * portfolio_df['Price_T2']
portfolio_value_T2 = portfolio_df['Portfolio_Value_T2'].sum()
portfolio_delta = portfolio_value_T2 - total_investment
portfolio_return_pct = (portfolio_delta / total_investment) * 100

print('Total Investment:', total_investment)
print('Final Portfolio Value:', portfolio_value_T2)
print('Profit/Loss:', portfolio_delta)
print('Portfolio Return Percentage:', portfolio_return_pct)
