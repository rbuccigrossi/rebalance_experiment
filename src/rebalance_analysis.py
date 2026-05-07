import csv
import os
from datetime import datetime, timedelta

def load_data(etf_list, data_dir='data'):
    data = {}
    for etf in etf_list:
        filepath = os.path.join(data_dir, f"{etf}_Close.csv")
        with open(filepath, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # Handle potential non-standard space in header
            price_col = next(col for col in reader.fieldnames if 'Adj Close' in col)
            for row in reader:
                date_str = row['Date'].strip()
                price = float(row[price_col])
                if date_str not in data:
                    data[date_str] = {}
                data[date_str][etf] = price
    return data

def get_sorted_dates(data, start_date, end_date):
    dates = [d for d in data.keys() if start_date <= d <= end_date]
    dates.sort()
    return dates

def run_simulation(etfs, data, sorted_dates, target_allocation, rebalance_freq=None):
    # Initial setup
    initial_cash = 10000.0
    start_date = sorted_dates[0]
    prices = data[start_date]

    # Calculate initial shares
    shares = {}
    for etf, weight in target_allocation.items():
        shares[etf] = (initial_cash * weight) / prices[etf]

    last_rebalance_date = datetime.strptime(start_date, '%Y-%m-%d')

    for i in range(1, len(sorted_dates)):
        current_date_str = sorted_dates[i]
        current_date = datetime.strptime(current_date_str, '%Y-%m-%d')

        should_rebalance = False
        if rebalance_freq == 'daily':
            should_rebalance = True
        elif rebalance_freq == 'weekly':
            if current_date - last_rebalance_date >= timedelta(weeks=1):
                should_rebalance = True
        elif rebalance_freq == 'monthly':
            if current_date.month != last_rebalance_date.month or current_date.year != last_rebalance_date.year:
                should_rebalance = True
        elif rebalance_freq == 'quarterly':
            if (current_date.month - 1) // 3 != (last_rebalance_date.month - 1) // 3 or current_date.year != last_rebalance_date.year:
                should_rebalance = True
        elif rebalance_freq == 'semi-annually':
            if (current_date.month - 1) // 6 != (last_rebalance_date.month - 1) // 6 or current_date.year != last_rebalance_date.year:
                should_rebalance = True
        elif rebalance_freq == 'annually':
            if current_date.year != last_rebalance_date.year:
                should_rebalance = True

        if should_rebalance:
            current_prices = data[current_date_str]
            total_value = sum(shares[etf] * current_prices[etf] for etf in etfs)
            for etf, weight in target_allocation.items():
                shares[etf] = (total_value * weight) / current_prices[etf]
            last_rebalance_date = current_date

    # Final value
    final_prices = data[sorted_dates[-1]]
    final_value = sum(shares[etf] * final_prices[etf] for etf in etfs)
    return final_value

def main():
    etfs = ['SPY', 'AGG', 'IJR', 'EEM']
    target_allocation = {
        'SPY': 0.50,
        'AGG': 0.20,
        'IJR': 0.15,
        'EEM': 0.15
    }

    data = load_data(etfs)
    start_date = '2004-01-02'
    end_date = '2026-05-05'
    sorted_dates = get_sorted_dates(data, start_date, end_date)

    scenarios = [
        ('Buy and Hold', None),
        ('Daily', 'daily'),
        ('Weekly', 'weekly'),
        ('Monthly', 'monthly'),
        ('Quarterly', 'quarterly'),
        ('Semi-Annually', 'semi-annually'),
        ('Annually', 'annually')
    ]

    print(f"Portfolio Simulation: {start_date} to {end_date}")
    print(f"Initial Investment: $10,000")
    print(f"Target Allocation: {target_allocation}")
    print("-" * 50)
    print(f"{'Scenario':<20} {'Final Value':<15}")
    print("-" * 50)

    for name, freq in scenarios:
        final_val = run_simulation(etfs, data, sorted_dates, target_allocation, freq)
        print(f"{name:<20} ${final_val:,.2f}")

if __name__ == "__main__":
    main()
