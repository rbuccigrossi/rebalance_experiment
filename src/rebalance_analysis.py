import csv
import os
from datetime import datetime, timedelta
import statistics

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

def get_sorted_dates(data):
    dates = list(data.keys())
    dates.sort()
    return dates

def find_closest_date(target_date_str, sorted_dates):
    """Finds the closest available trading day on or after the target date."""
    for date_str in sorted_dates:
        if date_str >= target_date_str:
            return date_str
    return sorted_dates[-1]

def run_simulation(etfs, data, sorted_dates, target_allocation, start_date_str, end_date_str, rebalance_freq=None):
    # Filter dates for this specific window
    window_dates = [d for d in sorted_dates if start_date_str <= d <= end_date_str]
    if not window_dates:
        return 0.0

    # Initial setup
    initial_cash = 10000.0
    actual_start_date = window_dates[0]
    prices = data[actual_start_date]

    # Calculate initial shares
    shares = {}
    for etf, weight in target_allocation.items():
        shares[etf] = (initial_cash * weight) / prices[etf]

    last_rebalance_date = datetime.strptime(actual_start_date, '%Y-%m-%d')

    for i in range(1, len(window_dates)):
        current_date_str = window_dates[i]
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
    final_prices = data[window_dates[-1]]
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
    sorted_dates = get_sorted_dates(data)

    # Define start and end range for rolling windows
    start_range_begin = datetime(2004, 1, 5)
    start_range_end = datetime(2016, 5, 2)

    scenarios = [
        ('Buy and Hold', None),
        ('Daily', 'daily'),
        ('Weekly', 'weekly'),
        ('Monthly', 'monthly'),
        ('Quarterly', 'quarterly'),
        ('Semi-Annually', 'semi-annually'),
        ('Annually', 'annually')
    ]

    results = {name: [] for name, _ in scenarios}

    current_monday = start_range_begin
    window_count = 0

    print(f"Running rolling 10-year window simulation...")

    while current_monday <= start_range_end:
        start_date_str = find_closest_date(current_monday.strftime('%Y-%m-%d'), sorted_dates)

        # 10 years later
        target_end_date = current_monday + timedelta(days=365 * 10 + 2) # Adding a couple days for leap years
        end_date_str = find_closest_date(target_end_date.strftime('%Y-%m-%d'), sorted_dates)

        for name, freq in scenarios:
            final_val = run_simulation(etfs, data, sorted_dates, target_allocation, start_date_str, end_date_str, freq)
            results[name].append(final_val)

        current_monday += timedelta(weeks=1)
        window_count += 1

    print("-" * 75)
    print(f"{'Scenario':<20} {'Avg Final Value':<20} {'Std Dev':<15} {'Count':<5}")
    print("-" * 75)

    for name, _ in scenarios:
        vals = results[name]
        avg = statistics.mean(vals)
        std_dev = statistics.stdev(vals) if len(vals) > 1 else 0
        print(f"{name:<20} ${avg:,.2f} {' ' * 5} ${std_dev:,.2f} {' ' * 5} {len(vals)}")

if __name__ == "__main__":
    main()
