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

### 1. Rolling 10-Year Window Rebalancing Simulation

To capture market volatility and reduce bias from specific time periods, we perform a rolling window analysis on rebalancing frequency.

- **Start Range**: Every Monday from January 5, 2004, to May 2, 2016.
- **Duration**: Each window spans 10 years.
- **Target Allocation**: 50% SPY, 20% AGG, 15% IJR, 15% EEM.
- **Scenarios**: Buy and Hold, Daily, Weekly, Monthly, Quarterly, Semi-Annually, Annually.

### 2. Rolling 10-Year Window Target Allocation Analysis

Using a fixed rebalancing frequency (Quarterly), we compare different asset allocations.

- **Start Range**: Every Monday from January 5, 2004, to May 2, 2016.
- **Duration**: Each window spans 10 years.
- **Rebalancing Frequency**: Quarterly.
- **Allocations Tested**:
    - 100% SPY
    - 75% SPY, 25% AGG
    - 50% SPY, 50% AGG
    - 50% SPY, 30% AGG, 10% IJR, 10% EEM
    - 50% SPY, 20% AGG, 15% IJR, 15% EEM
    - 50% SPY, 10% AGG, 20% IJR, 20% EEM

## Directory Structure

- `data/`: Contains the raw Excel and CSV files for the ETFs.
- `src/`: Python source code for data processing and analysis.
- `results/`: Output files and analysis results.

## How to Run

### 1. Data Verification
```bash
python3 src/verify_data.py
```

### 2. Rebalancing Frequency Analysis
```bash
python3 src/rebalance_analysis.py
```

### 3. Target Allocation Analysis
```bash
python3 src/allocation_analysis.py
```
