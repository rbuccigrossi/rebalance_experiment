import statistics
from datetime import datetime, timedelta
from simulation_engine import load_data, get_sorted_dates, find_closest_date, run_simulation

def main():
    etfs = ['SPY', 'GLD']

    # Target allocations to test
    allocations = [
        {'name': '100% SPY', 'weights': {'SPY': 1.0, 'GLD': 0.0}},
        {'name': '80/20 SPY/GLD', 'weights': {'SPY': 0.8, 'GLD': 0.2}},
        {'name': '60/40 SPY/GLD', 'weights': {'SPY': 0.6, 'GLD': 0.4}},
        {'name': '40/60 SPY/GLD', 'weights': {'SPY': 0.4, 'GLD': 0.6}},
        {'name': '20/80 SPY/GLD', 'weights': {'SPY': 0.2, 'GLD': 0.8}},
        {'name': '100% GLD', 'weights': {'SPY': 0.0, 'GLD': 1.0}},
    ]

    data = load_data(etfs)
    sorted_dates = get_sorted_dates(data)

    # Define start and end range for rolling windows
    start_range_begin = datetime(2004, 12, 6)
    start_range_end = datetime(2016, 5, 2)

    rebalance_freq = 'quarterly'

    results = {a['name']: [] for a in allocations}

    current_monday = start_range_begin

    print(f"Running rolling 10-year window simulation for target allocations...")
    print(f"Fixed rebalancing frequency: {rebalance_freq}")

    while current_monday <= start_range_end:
        start_date_str = find_closest_date(current_monday.strftime('%Y-%m-%d'), sorted_dates)

        # 10 years later
        target_end_date = current_monday + timedelta(days=365 * 10 + 2)
        end_date_str = find_closest_date(target_end_date.strftime('%Y-%m-%d'), sorted_dates)

        for alloc in allocations:
            final_val = run_simulation(etfs, data, sorted_dates, alloc['weights'], start_date_str, end_date_str, rebalance_freq)
            results[alloc['name']].append(final_val)

        current_monday += timedelta(weeks=1)

    print("-" * 90)
    print(f"{'Allocation Scenario':<25} {'Avg Final Value':<20} {'Std Dev':<15} {'Count':<5}")
    print("-" * 90)

    for alloc in allocations:
        name = alloc['name']
        vals = results[name]
        avg = statistics.mean(vals)
        std_dev = statistics.stdev(vals) if len(vals) > 1 else 0
        print(f"{name:<25} ${avg:,.2f} {' ' * 5} ${std_dev:,.2f} {' ' * 5} {len(vals)}")

if __name__ == "__main__":
    main()
