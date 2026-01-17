import pandas as pd
import numpy as np
import os

DATA_PATH = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/BTCUSDT_1d_LIVE_UPDATE.csv" 
# Use Daily data
# If missing, use 15m and resample

COST_TAKER = 0.0004
SLIPPAGE = 0.0001

def load_data(path):
    if not os.path.exists(path):
        # Fallback
        path = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/BTCUSDT_15m_2024-01-01_2025-12-31.csv"
        df = pd.read_csv(path)
        df.columns = [c.lower() for c in df.columns]
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        return df.resample('D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
        
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df

def run_strategy(df):
    data = df.copy()
    data['day_of_week'] = data.index.dayofweek
    # 0=Mon, 4=Fri, 5=Sat, 6=Sun
    
    # Logic: Long Friday Close (Postion=1 on Sat/Sun)
    # Entry: Friday Close (so Position=1 on Saturday 00:00)
    # Exit: Sunday Close (so Position=0 on Monday 00:00)
    
    # Position:
    # If Day is 5 (Sat) or 6 (Sun), Position = 1.
    # Else 0.
    
    data['position'] = np.where(data['day_of_week'].isin([5, 6]), 1, 0)
    
    # Returns
    # Position shifted?
    # Position=1 on Sat means we hold Sat candle.
    # Sat candle is Index=Sat.
    # So we don't shift?
    # Let's verify.
    # Return at T is (Close T - Close T-1).
    # If we want to capture Return T, we must hold at T-1 Close.
    # So Position[T-1] should be 1.
    # If Position[Sat] = 1.
    # Then Position.shift(1) at Sun is 1.
    # We capture Sun return.
    # We want to capture Sat return too.
    # So Position[Fri] must be 1.
    # But logic says `day.isin([5,6])`.
    # Friday is 4.
    # So Position[4] = 0.
    # Then Strat captures Sun Return (Pos[5]=1) but misses Sat Return (Pos[4]=0).
    # Fix: Set Position=1 if Day is 5 or 6 -> Shift(-1)?
    # Or just logical shift:
    # We want to hold over the weekend.
    # Hold FROM Friday Close TO Sunday Close.
    # This covers Sat and Sun candles.
    # So we need Position[Fri]=1, Position[Sat]=1.
    # Position[Sun]=0 (Exit at Sun Close).
    
    target_days = [4, 5] # Fri, Sat
    data['position'] = np.where(data['day_of_week'].isin(target_days), 1, 0)
    
    data['ret'] = data['close'].pct_change()
    data['strat_ret'] = data['position'].shift(1) * data['ret']
    
    data['trades'] = data['position'].diff().abs().fillna(0)
    data['costs'] = data['trades'] * (COST_TAKER + SLIPPAGE)
    data['net_ret'] = data['strat_ret'] - data['costs']
    return data

def calc_stats(returns):
    n = 365
    if returns.std() == 0: return 0, 0, 0
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n)
    cum = (1+returns).cumprod()
    tot = cum.iloc[-1]-1
    mdd = ((cum - cum.cummax())/cum.cummax()).min()
    return tot, sharpe, mdd

if __name__ == "__main__":
    df = load_data(DATA_PATH)
    res = run_strategy(df)
    tot, sh, mdd = calc_stats(res['net_ret'])
    print(f"Weekend Long")
    print(f"Ret: {tot:.2%}, Sharpe: {sh:.4f}, MDD: {mdd:.2%}")
