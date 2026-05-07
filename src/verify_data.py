import csv
import os

def get_date_range(filepath):
    dates = []
    with open(filepath, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get('Date')
            if date_str:
                dates.append(date_str.strip())

    if not dates:
        return None, None

    # Sort dates to find the range. Note: dates are in YYYY-MM-DD format
    dates.sort()
    return dates[0], dates[-1]

def main():
    etfs = ['AGG', 'EEM', 'IJR', 'SPY']
    data_dir = 'data'

    print(f"{'ETF':<10} {'Start Date':<15} {'End Date':<15}")
    print("-" * 40)

    for etf in etfs:
        filename = f"{etf}_Close.csv"
        filepath = os.path.join(data_dir, filename)

        if os.path.exists(filepath):
            start_date, end_date = get_date_range(filepath)
            print(f"{etf:<10} {start_date:<15} {end_date:<15}")
        else:
            print(f"{etf:<10} File not found: {filename}")

if __name__ == "__main__":
    main()
