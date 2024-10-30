import pandas as pd

# Create the data as a list of dictionaries
data = [
    # Left table
    {"Ticker": "GLYC", "Last": 0.49, "Change": 191.32, "Volume": "1.12B", "Signal": "Top Gainers"},
    {"Ticker": "BKYI", "Last": 1.22, "Change": 76.81, "Volume": "120.12M", "Signal": "Top Gainers"},
    {"Ticker": "LIXT", "Last": 2.08, "Change": 58.78, "Volume": "32.82M", "Signal": "Top Gainers"},
    {"Ticker": "WGS", "Last": 84.02, "Change": 49.88, "Volume": "3.25M", "Signal": "Top Gainers"},
    {"Ticker": "PFIE", "Last": 2.50, "Change": 46.20, "Volume": "29.92M", "Signal": "Top Gainers"},
    {"Ticker": "LTBR", "Last": 12.31, "Change": 35.57, "Volume": "15.61M", "Signal": "New High"},
    {"Ticker": "WGS", "Last": 84.02, "Change": 49.88, "Volume": "3.25M", "Signal": "New High"},
    {"Ticker": "PFIE", "Last": 2.50, "Change": 46.20, "Volume": "29.92M", "Signal": "New High"},
    {"Ticker": "OPRA", "Last": 13.57, "Change": 10.08, "Volume": "3.00M", "Signal": "New High"},
    {"Ticker": "BLTE", "Last": 69.78, "Change": 2.94, "Volume": "90.00K", "Signal": "Overbought"},
    {"Ticker": "GLYC", "Last": 0.49, "Change": 191.32, "Volume": "1.12B", "Signal": "Unusual Volume"},
    {"Ticker": "LIXT", "Last": 2.08, "Change": 58.78, "Volume": "32.82M", "Signal": "Unusual Volume"},
    {"Ticker": "JL", "Last": 0.80, "Change": 69.85, "Volume": "40.07M", "Signal": "Unusual Volume"},
    {"Ticker": "KOF", "Last": 84.46, "Change": 0.07, "Volume": "159.17K", "Signal": "Upgrades"},
    {"Ticker": "ABG", "Last": 231.42, "Change": 2.59, "Volume": "351.53K", "Signal": "Earnings Before"},
    {"Ticker": "HMC", "Last": 13.72, "Change": 0.37, "Volume": "604.15K", "Signal": "Insider Buying"},
    
    # Right table
    {"Ticker": "PLRZ", "Last": 1.55, "Change": -64.61, "Volume": "1.43M", "Signal": "Top Losers"},
    {"Ticker": "EFSH", "Last": 0.48, "Change": -61.90, "Volume": "19.14M", "Signal": "Top Losers"},
    {"Ticker": "TMDX", "Last": 88.50, "Change": -29.90, "Volume": "11.67M", "Signal": "Top Losers"},
    {"Ticker": "JBI", "Last": 7.24, "Change": -29.78, "Volume": "21.25M", "Signal": "Top Losers"},
    {"Ticker": "PGHL", "Last": 13.80, "Change": -27.75, "Volume": "318.05K", "Signal": "Top Losers"},
    {"Ticker": "COYA", "Last": 7.37, "Change": -27.67, "Volume": "909.13K", "Signal": "Top Losers"},
    {"Ticker": "DBGI", "Last": 0.10, "Change": -33.83, "Volume": "20.44M", "Signal": "New Low"},
    {"Ticker": "LILM", "Last": 0.10, "Change": -30.84, "Volume": "82.10M", "Signal": "New Low"},
    {"Ticker": "ADTX", "Last": 0.59, "Change": -18.07, "Volume": "2.93M", "Signal": "New Low"},
    {"Ticker": "CPRI", "Last": 20.48, "Change": -4.25, "Volume": "9.18M", "Signal": "Oversold"},
    {"Ticker": "CETX", "Last": 0.30, "Change": 9.97, "Volume": "49.02M", "Signal": "Oversold"},
    {"Ticker": "UPXI", "Last": 8.55, "Change": 27.04, "Volume": "10.32M", "Signal": "Most Volatile"},
    {"Ticker": "MMA", "Last": 2.21, "Change": -3.45, "Volume": "917.36K", "Signal": "Most Volatile"},
    {"Ticker": "GLYC", "Last": 0.49, "Change": 191.32, "Volume": "1.12B", "Signal": "Most Active"},
    {"Ticker": "VCIG", "Last": 0.09, "Change": 23.24, "Volume": "315.45M", "Signal": "Most Active"},
    {"Ticker": "CE", "Last": 126.88, "Change": -2.38, "Volume": "811.02K", "Signal": "Downgrades"},
    {"Ticker": "AAT", "Last": 27.34, "Change": -0.40, "Volume": "154.89K", "Signal": "Earnings After"},
    {"Ticker": "RBRK", "Last": 42.60, "Change": 4.98, "Volume": "2.97M", "Signal": "Insider Selling"}
]

# Create DataFrame
df = pd.DataFrame(data)

# Convert Volume to numeric by removing 'B', 'M', 'K' and converting to numbers
def convert_volume(vol_str):
    if isinstance(vol_str, str):
        if 'B' in vol_str:
            return float(vol_str.replace('B', '')) * 1e9
        elif 'M' in vol_str:
            return float(vol_str.replace('M', '')) * 1e6
        elif 'K' in vol_str:
            return float(vol_str.replace('K', '')) * 1e3
    return float(vol_str)

# Convert Volume column
df['Volume'] = df['Volume'].apply(convert_volume)

# Sort DataFrame by Change percentage in descending order
df = df.sort_values('Change', ascending=False)

# Reset index
df = df.reset_index(drop=True)

print(df)