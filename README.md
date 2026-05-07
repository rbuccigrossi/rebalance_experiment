# ETF Rebalancing Analysis

This project explores historical data for four Exchange Traded Funds (ETFs) to determine the optimal rebalancing periodicity and asset allocation.

## ETFs Analyzed

- **SPY**: US S&P 500 large caps
- **IJR**: US small caps
- **EEM**: Emerging markets
- **AGG**: US bond aggregate

The data includes Adjusted Close prices, which account for dividend reinvestment.

## Project Goals

1.  **Optimal Rebalancing Periodicity**: Determine the best time-based rebalancing frequency (e.g., monthly, quarterly, annually) based on historical performance.
2.  **Optimal Target Allocation**: Given the best rebalancing frequency, identify the target asset allocation among the four ETFs that yields the best results.

## Directory Structure

- `data/`: Contains the raw Excel and CSV files for the ETFs.
- `src/`: Python source code for data processing and analysis.
- `results/`: Output files and analysis results.

## Data Verification

A script `src/verify_data.py` is provided to verify the date ranges and integrity of the source CSV files.
