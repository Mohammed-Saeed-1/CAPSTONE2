# stock_simulation_app/monte_carlo_simulation.py
import yfinance as yf
import numpy as np

def perform_monte_carlo_simulation(stock_symbol):
    stock_data = yf.download(stock_symbol, period="10y")
    stock_data["Daily_Returns"] = stock_data["Adj Close"].pct_change()

    mean_return = stock_data["Daily_Returns"].mean()
    std_dev = stock_data["Daily_Returns"].std()

    initial_investment = 200
    investment_period_years = 1
    num_simulations = 1000

    final_values = []

    for _ in range(num_simulations):
        daily_returns = np.random.normal(mean_return, std_dev, investment_period_years * 252)
        final_value = initial_investment * np.prod(1 + daily_returns)
        final_values.append(final_value)

    mean_final_value = np.mean(final_values)
    std_dev_final_value = np.std(final_values)

    results = {
        'initial_investment': initial_investment,
        'investment_period_years': investment_period_years,
        'num_simulations': num_simulations,
        'mean_final_value': mean_final_value,
        'std_dev_final_value': std_dev_final_value,
    }

    return results
