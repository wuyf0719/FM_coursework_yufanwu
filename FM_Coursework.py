import yfinance as yf
import pandas as pd
import numpy as np

# Define Company & Time Period
stocks = ["AMZN", "NVDA"]
start_date = "2019-11-27"
end_date = "2024-11-27"

# Function to Download Stock Data
def download_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, interval="1d")
    data["Daily Return"] = data["Adj Close"].pct_change()  # ATTENTION!Daily Return
    return data

# Download & Save Data for Both Stocks
stock_data = {}
for stock in stocks:
    data = download_stock_data(stock, start_date, end_date)
    data.to_csv(f"{stock}_Daily_Price_Return.csv")
    stock_data[stock] = data
    print(f"{stock} data has been saved in {stock}_Daily_Price_Return.csv")

# Read Data
amzn = stock_data["AMZN"]
nvda = stock_data["NVDA"]

# Calculate Expected Returns & Standard Deviations
amzn_mean = amzn["Daily Return"].mean()
nvda_mean = nvda["Daily Return"].mean()

amzn_std = amzn["Daily Return"].std()
nvda_std = nvda["Daily Return"].std()

# Print Expected Returns & Standard Deviations
#Excel double-check
print("\nExpected Returns:")
print(f"AMZN: {amzn_mean:.6f}, NVDA: {nvda_mean:.6f}")
print("\nStandard Deviations:")
print(f"AMZN: {amzn_std:.6f}, NVDA: {nvda_std:.6f}")

# Calculate Correlation Coefficient
correlation = amzn["Daily Return"].corr(nvda["Daily Return"])
print(f"\nCorrelation Coefficient between AMZN and NVDA: {correlation:.6f}")

# Portfolio Analysis: Define Weights
weights = [(0.2, 0.8), (0.5, 0.5), (0.8, 0.2)]

# Portfolio Calculations
results = []
for w1, w2 in weights:
    portfolio_return = w1 * amzn_mean + w2 * nvda_mean
    portfolio_variance = (w1**2 * amzn_std**2 +
                          w2**2 * nvda_std**2 +
                          2 * w1 * w2 * correlation * amzn_std * nvda_std)
    portfolio_std = np.sqrt(portfolio_variance)
    results.append({
        "Weight_AMZN": w1,
        "Weight_NVDA": w2,
        "Portfolio Return": portfolio_return,
        "Portfolio Variance": portfolio_variance,
        "Portfolio Std Dev": portfolio_std
    })

# Include Individual Stock Metrics
stock_metrics = {
    "Stock": ["AMZN", "NVDA"],
    "Expected Return": [amzn_mean, nvda_mean],
    "Standard Deviation": [amzn_std, nvda_std]
}
stock_metrics_df = pd.DataFrame(stock_metrics)

# Combine Stock Metrics and Portfolio Analysis
results_df = pd.DataFrame(results)
final_df = pd.concat([stock_metrics_df, results_df], axis=1)

# Save Results
final_df.to_csv("Portfolio_Analysis_With_Stock_Metrics.csv", index=False)
print("\nPortfolio analysis with stock metrics has been saved in Portfolio_Analysis_With_Stock_Metrics.csv")