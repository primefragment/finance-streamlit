import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class NVDABacktest:
    @staticmethod
    def calculate_rsi(data, periods=14):
        """Calculate RSI without talib"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_ema(data, span=20):
        """Calculate EMA without talib"""
        return data.ewm(span=span, adjust=False).mean()

    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD without talib"""
        fast_ema = data.ewm(span=fast, adjust=False).mean()
        slow_ema = data.ewm(span=slow, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        macd_hist = macd - signal_line
        return macd, signal_line, macd_hist

    def __init__(self, initial_capital=100000):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.positions = 0
        self.trades = []
        self.equity_curve = []
        
    def fetch_data(self, start_date, end_date):
        """Fetch NVDA historical data and calculate technical indicators"""
        nvda = yf.download('NVDA', start=start_date, end=end_date)
        
        # Calculate technical indicators
        nvda['RSI'] = self.calculate_rsi(nvda['Close'])
        nvda['EMA20'] = self.calculate_ema(nvda['Close'], 20)
        macd, macdsignal, macdhist = self.calculate_macd(nvda['Close'])
        nvda['MACD'] = macd
        nvda['MACD_Signal'] = macdsignal
        nvda['MACD_Hist'] = macdhist
        
        print(nvda)

        return nvda
    
    def check_entry_conditions(self, row, prev_row):
        """Check if entry conditions are met"""
        conditions = [
            # row['Close'] > row['EMA20'],  # Price above 20 EMA
            (row['RSI'] < 30).all(),  # Oversold condition
            (row['MACD_Hist'] > prev_row['MACD_Hist']).all(),  # Positive MACD momentum
            (row['Volume'] > prev_row['Volume'] * 1.1).all()  # Volume increase
        ]
        return all(conditions)
    
    def calculate_position_size(self, price, stop_loss_pct=0.05):
        """Calculate position size based on risk management rules"""
        stop_loss_amount = self.capital * 0.05  # Risk 5% of capital
        stop_loss_points = price * stop_loss_pct
        shares = int(stop_loss_amount / stop_loss_points)
        max_shares = int(self.capital / price)  # Can't buy more than we can afford
        return min(shares, max_shares)
    
    def run_backtest(self, data):
        """Run the backtest on historical data"""
        for i in range(1, len(data)):
            current_row = data.iloc[i]
            prev_row = data.iloc[i-1]
            
            # Update equity curve
            if self.positions > 0:
                current_value = self.capital + (self.positions * current_row['Close'])
            else:
                current_value = self.capital
            self.equity_curve.append(current_value)
            
            # Check for exit if we have a position
            if self.positions > 0:
                entry_price = self.trades[-1]['entry_price']
                gain = (current_row['Close'] - entry_price) / entry_price
                
                # Exit conditions with trailing stop
                if gain.item() >= 0.10:  # Target reached
                    self.capital += self.positions * current_row['Close']
                    self.trades[-1].update({
                        'exit_price': current_row['Close'],
                        'exit_date': current_row.name,
                        'gain': gain,
                        'reason': 'target'
                    })
                    self.positions = 0
                elif gain.item() <= -0.05:  # Stop loss hit
                    self.capital += self.positions * current_row['Close']
                    self.trades[-1].update({
                        'exit_price': current_row['Close'],
                        'exit_date': current_row.name,
                        'gain': gain,
                        'reason': 'stop_loss'
                    })
                    self.positions = 0
            
            # Check for entry if we have no position
            elif self.positions == 0 and self.check_entry_conditions(current_row, prev_row):
                shares = self.calculate_position_size(current_row['Close'])
                if shares > 0:
                    self.positions = shares
                    self.capital -= shares * current_row['Close']
                    self.trades.append({
                        'entry_date': current_row.name,
                        'entry_price': current_row['Close'],
                        'shares': shares
                    })
    
    def generate_report(self):
        """Generate performance report"""
        if not self.trades:
            return "No trades executed"
            
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if (t.get('gain', 0) > 0).bool()])
        losing_trades = len([t for t in self.trades if (t.get('gain', 0) <= 0).bool()])
        
        if total_trades > 0:
            win_rate = winning_trades / total_trades
            gains = [t.get('gain', 0) for t in self.trades]
            avg_gain = np.mean(gains)
            # max_drawdown = self.calculate_max_drawdown()
            
            final_equity = self.equity_curve[-1]
            total_return = (final_equity - self.initial_capital) / self.initial_capital
            
            # Calculate additional metrics
            avg_winner = np.mean([g for g in gains if (g > 0).bool()]) if winning_trades > 0 else 0
            avg_loser = np.mean([g for g in gains if (g <= 0).bool()]) if losing_trades > 0 else 0
            
            return {
                'Total Trades': total_trades,
                'Winning Trades': winning_trades,
                'Losing Trades': losing_trades,
                'Win Rate': f"{win_rate:.2%}",
                'Average Gain': f"{avg_gain:.2%}",
                'Average Winner': f"{avg_winner:.2%}",
                'Average Loser': f"{avg_loser:.2%}",
                # 'Max Drawdown': f"{max_drawdown:.2%}",
                # 'Total Return': f"{total_return:.2%}",
                # 'Final Equity': f"${final_equity:,.2f}"
            }
    
    def calculate_max_drawdown(self):
        """Calculate maximum drawdown from equity curve"""
        peak = self.equity_curve[0]
        max_dd = 0
        
        for value in self.equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        
        return max_dd
    
    def plot_results(self):
        """Plot equity curve and trade points"""
        plt.figure(figsize=(15, 7))
        plt.plot(self.equity_curve, label='Equity Curve')
        
        # Plot trade points
        dates = pd.date_range(start=self.trades[0]['entry_date'], periods=len(self.equity_curve), freq='D')
        
        for trade in self.trades:
            entry_idx = (trade['entry_date'] - dates[0]).days
            if 'exit_date' in trade:
                exit_idx = (trade['exit_date'] - dates[0]).days
                color = 'g' if trade['gain'] > 0 else 'r'
                plt.plot([entry_idx, exit_idx], 
                        [self.equity_curve[entry_idx], self.equity_curve[exit_idx]], 
                        color=color, linewidth=2)
        
        plt.title('NVDA Trading Strategy Backtest Results')
        plt.xlabel('Days')
        plt.ylabel('Portfolio Value ($)')
        plt.grid(True)
        plt.legend()
        plt.show()

# Example usage
def run_strategy(initial_capital=100000, start_date='2023-01-01', end_date='2024-01-01'):
    backtest = NVDABacktest(initial_capital=initial_capital)
    data = backtest.fetch_data(start_date, end_date)
    backtest.run_backtest(data)
    report = backtest.generate_report()
    print("\nBacktest Results:")
    for key, value in report.items():
        print(f"{key}: {value}")
    backtest.plot_results()
    return backtest

if __name__ == "__main__":
    backtest = run_strategy()