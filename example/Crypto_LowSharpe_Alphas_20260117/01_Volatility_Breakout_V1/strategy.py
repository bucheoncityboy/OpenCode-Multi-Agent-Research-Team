import pandas as pd
import numpy as np
import os
import sys

# -----------------------------------------------------------------------------
# 1. Configuration
# -----------------------------------------------------------------------------
DATA_PATH = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/BTCUSDT_15m_2024-01-01_2025-12-31.csv"
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
COST_MAKER = 0.0002
COST_TAKER = 0.0004
SLIPPAGE = 0.0001
INITIAL_CAPITAL = 10000

# Strategy Parameters
K = 0.5  # Range multiplier

# -----------------------------------------------------------------------------
# 2. Data Loading & Preprocessing
# -----------------------------------------------------------------------------
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data not found: {path}")
    
    df = pd.read_csv(path)
    # Check column names and standardize
    df.columns = [c.lower() for c in df.columns]
    
    # Parse dates
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    
    df.sort_index(inplace=True)
    
    # Required columns
    req_cols = ['open', 'high', 'low', 'close', 'volume']
    for c in req_cols:
        if c not in df.columns:
            raise ValueError(f"Missing column: {c}")
            
    return df

# -----------------------------------------------------------------------------
# 3. Strategy Logic (Vectorized)
# -----------------------------------------------------------------------------
def run_strategy(df):
    data = df.copy()
    
    # Resample to Daily to get Previous Day's Range
    daily_df = data.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })
    
    # Calculate Range
    daily_df['range'] = daily_df['high'] - daily_df['low']
    
    # Shift(1) is CRITICAL to avoid look-ahead bias
    # We use Yesterday's Range and Yesterday's Open (or Today's Open if logic dictates)
    # Standard Vol Breakout: Buy if Price > Today's Open + K * Yesterday's Range
    
    daily_df['prev_range'] = daily_df['range'].shift(1)
    
    # Reindex back to 15m timeframe (forward fill daily values)
    # Note: reindex method
    aligned_range = daily_df['prev_range'].reindex(data.index, method='ffill')
    aligned_daily_open = daily_df['open'].reindex(data.index, method='ffill')
    
    data['target_long'] = aligned_daily_open + (aligned_range * K)
    data['target_short'] = aligned_daily_open - (aligned_range * K)
    
    # Signal Generation
    # Entry: Close breaks target
    # Exit: End of Day (simplified for 15m: exit if new day starts? Or just hold?)
    # Let's implement simple "Always in market" or "Hold until Stop" first.
    # Original Request: "Buy if Price > Open + K*Range"
    
    data['signal'] = 0
    data.loc[data['close'] > data['target_long'], 'signal'] = 1
    data.loc[data['close'] < data['target_short'], 'signal'] = -1
    
    # Position: shift(1) of signal? 
    # If signal triggers at Close of T, we enter at Open of T+1?
    # Or assuming we enter at Close of T (slippage accounts for it).
    # Let's use position logic: Maintain position until flip.
    
    data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
    
    # Apply Shift(1) to Position for PnL calculation (Entered at T, PnL starts T+1)
    data['strategy_returns'] = data['position'].shift(1) * data['close'].pct_change()
    
    # Costs
    # We trade when position changes
    data['trades'] = data['position'].diff().abs().fillna(0)
    data['costs'] = data['trades'] * (COST_TAKER + SLIPPAGE)
    
    data['net_returns'] = data['strategy_returns'] - data['costs']
    
    return data

# -----------------------------------------------------------------------------
# 4. Performance Metrics
# -----------------------------------------------------------------------------
def calculate_metrics(returns):
    # Annualized Sharpe (assume 15m data = 96 periods per day * 365 days)
    # Actually simple: mean(ret) / std(ret) * sqrt(periods)
    
    n_periods = 365 * 96
    
    cum_ret = (1 + returns).cumprod()
    total_ret = cum_ret.iloc[-1] - 1
    
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n_periods) if returns.std() != 0 else 0
    
    # MDD
    rolling_max = cum_ret.cummax()
    drawdown = (cum_ret - rolling_max) / rolling_max
    mdd = drawdown.min()
    
    # Win Rate
    # Calculate per-trade returns (needs trade list)
    # Simplified here: Win Rate of Intervals (not accurate for trade-based win rate)
    # Let's extract trades for trade-based metrics
    
    return {
        "Total Return": total_ret,
        "Sharpe": sharpe,
        "MDD": mdd
    }

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Loading data from {DATA_PATH}...")
    try:
        df = load_data(DATA_PATH)
        df = df[START_DATE:END_DATE]
        print(f"Data Loaded: {len(df)} rows")
        
        result_df = run_strategy(df)
        metrics = calculate_metrics(result_df['net_returns'])
        
        print("-" * 30)
        print("Strategy Performance Report")
        print("-" * 30)
        print(f"Total Return: {metrics['Total Return']:.2%}")
        print(f"Sharpe Ratio: {metrics['Sharpe']:.4f}")
        print(f"Max Drawdown: {metrics['MDD']:.2%}")
        print("-" * 30)
        
        # Validation Check
        if metrics['Sharpe'] > 0.2:
            print("[SUCCESS] Sharpe criteria met (> 0.2)")
        else:
            print("[FAIL] Sharpe too low")
            
    except Exception as e:
        print(f"Error: {e}")
