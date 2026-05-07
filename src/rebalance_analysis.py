import statistics
from datetime import datetime, timedelta
from simulation_engine import load_data, get_sorted_dates, find_closest_date, run_simulation

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

    print(f"Running rolling 10-year window simulation for rebalancing frequency...")

    while current_monday <= start_range_end:
        start_date_str = find_closest_date(current_monday.strftime('%Y-%m-%d'), sorted_dates)

        # 10 years later
        target_end_date = current_monday + timedelta(days=365 * 10 + 2)
        end_date_str = find_closest_date(target_end_date.strftime('%Y-%m-%d'), sorted_dates)

        for name, freq in scenarios:
            final_val = run_simulation(etfs, data, sorted_dates, target_allocation, start_date_str, end_date_str, freq)
            results[name].append(final_val)

        current_monday += timedelta(weeks=1)

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
