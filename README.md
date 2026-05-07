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

## Experiments

### Rolling 10-Year Window Simulation

To capture market volatility and reduce bias from specific time periods (like recent market spikes), we perform a rolling window analysis.

- **Start Range**: Every Monday from January 5, 2004, to May 2, 2016.
- **Duration**: Each window spans 10 years (approx. 248 windows in total).
- **Initial Investment**: $10,000.
- **Target Allocation**: 50% SPY, 20% AGG, 15% IJR, 15% EEM.
- **Scenarios**:
    - Buy and Hold (No rebalancing)
    - Daily
    - Weekly
    - Monthly
    - Quarterly
    - Semi-Annually
    - Annually

The script calculates the average final portfolio value and the standard deviation (variance) for each scenario across all windows.

## Directory Structure

- `data/`: Contains the raw Excel and CSV files for the ETFs.
- `src/`: Python source code for data processing and analysis.
- `results/`: Output files and analysis results.

## How to Run

### 1. Data Verification
Verify the date ranges and integrity of the source CSV files:
```bash
python3 src/verify_data.py
```

### 2. Rebalancing Analysis
Run the rolling 10-year window simulation:
```bash
python3 src/rebalance_analysis.py
```
The results will display the average final value and standard deviation for each rebalancing approach.
