import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data(start_date, end_date):
        """Fetch NVDA historical data and calculate technical indicators"""
        nvda = yf.download('NVDA', start=start_date, end=end_date)
        print(nvda)
        

def run_strategy(initial_capital=100000, start_date='2023-01-01', end_date='2024-01-01'):
    # backtest = NVDABacktest(initial_capital=initial_capital)
    data = fetch_data(start_date, end_date)
    # backtest.run_backtest(data)
    # report = backtest.generate_report()
    # print("\nBacktest Results:")
    # for key, value in report.items():
    #     print(f"{key}: {value}")
    # backtest.plot_results()
    # return backtest

if __name__ == "__main__":
    run_strategy()