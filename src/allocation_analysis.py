import statistics
from datetime import datetime, timedelta
from simulation_engine import load_data, get_sorted_dates, find_closest_date, run_simulation

def main():
    etfs = ['SPY', 'AGG', 'IJR', 'EEM']

    # Target allocations to test
    allocations = [
        {'name': '100% SPY', 'weights': {'SPY': 1.0, 'AGG': 0.0, 'IJR': 0.0, 'EEM': 0.0}},
        {'name': '75/25 SPY/AGG', 'weights': {'SPY': 0.75, 'AGG': 0.25, 'IJR': 0.0, 'EEM': 0.0}},
        {'name': '50/50 SPY/AGG', 'weights': {'SPY': 0.5, 'AGG': 0.5, 'IJR': 0.0, 'EEM': 0.0}},
        {'name': '50/30/10/10 Split', 'weights': {'SPY': 0.5, 'AGG': 0.3, 'IJR': 0.1, 'EEM': 0.1}},
        {'name': '50/20/15/15 Split', 'weights': {'SPY': 0.5, 'AGG': 0.2, 'IJR': 0.15, 'EEM': 0.15}},
        {'name': '50/10/20/20 Split', 'weights': {'SPY': 0.5, 'AGG': 0.1, 'IJR': 0.2, 'EEM': 0.2}},
    ]

    data = load_data(etfs)
    sorted_dates = get_sorted_dates(data)

    # Define start and end range for rolling windows
    start_range_begin = datetime(2004, 1, 5)
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
