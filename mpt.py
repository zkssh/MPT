# Import necessary libraries
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Function to load data and calculate returns
def load_data(filename):
    data = pd.read_csv(filename)
    data['Return'] = data['Close'].pct_change()
    return data

# Load the data from CSV files
btc_data = load_data('BTC-USD.csv')
eth_data = load_data('ETH-USD.csv')
sol_data = load_data('SOL-USD.csv')
link_data = load_data('LINK-USD.csv')

# Combine returns into a single DataFrame
returns = pd.DataFrame({
    'BTC': btc_data['Return'],
    'ETH': eth_data['Return'],
    'SOL': sol_data['Return'],
    'LINK': link_data['Return']
})

# Drop missing values
returns.dropna(inplace=True)

# Calculate mean returns and covariance matrix
mean_returns = returns.mean() * 365  # Annualize returns
cov_matrix = returns.cov() * 365  # Annualize covariances

# Set the number of portfolios to simulate
num_portfolios = 10000

# Initialize arrays for portfolio weights, returns, volatility, and Sharpe ratio
weights_array = np.zeros((num_portfolios, len(mean_returns)))
returns_array = np.zeros(num_portfolios)
volatility_array = np.zeros(num_portfolios)
sharpe_ratio_array = np.zeros(num_portfolios)

# Assume risk-free rate is close to zero (for simplicity)
risk_free_rate = 0.001

# Simulate random portfolio weights and calculate performance metrics
for i in range(num_portfolios):
    weights = np.random.random(len(mean_returns))
    weights /= np.sum(weights)
    weights_array[i, :] = weights
    returns_array[i] = np.dot(weights, mean_returns)
    volatility_array[i] = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio_array[i] = (returns_array[i] - risk_free_rate) / volatility_array[i]

# Efficient Frontier Calculation with Weights
efficient_frontier_data = []
for vol, ret, sharpe, weight in zip(volatility_array, returns_array, sharpe_ratio_array, weights_array):
    if not efficient_frontier_data or ret > efficient_frontier_data[-1]['ret']:
        efficient_frontier_data.append({'ret': ret, 'vol': vol, 'sharpe': sharpe, 'weights': weight})

# Extract information for plotting
efficient_returns = [data['ret'] for data in efficient_frontier_data]
efficient_volatility = [data['vol'] for data in efficient_frontier_data]
efficient_text = [
    f"BTC: {data['weights'][0]:.2%}, ETH: {data['weights'][1]:.2%}, SOL: {data['weights'][2]:.2%}, LINK: {data['weights'][3]:.2%}"
    for data in efficient_frontier_data
]

# Plot the portfolios
scatter = go.Scatter(
    x=volatility_array, y=returns_array,
    mode='markers',
    marker=dict(color=sharpe_ratio_array, colorscale='Viridis', size=5, showscale=True),
    name='Portfolios'
)

# Plot the efficient frontier
efficient_frontier = go.Scatter(
    x=efficient_volatility, y=efficient_returns,
    mode='lines+markers',
    line=dict(color='magenta', width=4),
    name='Efficient Frontier',
    text=efficient_text,
    hoverinfo='text'
)

# Create and show the figure
fig = go.Figure(data=[scatter, efficient_frontier])
fig.update_layout(
    title='Portfolio Optimization with Efficient Frontier',
    xaxis_title='Volatility (Standard Deviation)',
    yaxis_title='Expected Return',
    hovermode='closest'
)
fig.show()

