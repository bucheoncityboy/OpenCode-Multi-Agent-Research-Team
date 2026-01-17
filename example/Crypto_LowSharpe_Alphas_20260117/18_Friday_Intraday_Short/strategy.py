import pandas as pd
import numpy as np
import os

DATA_PATH = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/BTCUSDT_1d_LIVE_UPDATE.csv" 
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
        # Resample Daily
        return df.resample('D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()

    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    return df

def run_strategy(df):
    data = df.copy()
    data['day_of_week'] = data.index.dayofweek
    # Friday = 4
    
    # Logic: Short Friday Open, Cover Friday Close.
    # Return = (Open - Close) / Open
    # But we work with Close-to-Close series usually.
    # If we use Daily Data:
    # We can calculate (Open - Close) directly.
    # Signal: If Day=4.
    
    # Vectorized:
    # Ret = (Open - Close) / Open if Day=4 else 0.
    # Note: Shorting means (Open - Close).
    
    data['strat_ret'] = np.where(data['day_of_week'] == 4, (data['open'] - data['close']) / data['open'], 0)
    
    # Costs
    # 2 trades per Friday.
    data['costs'] = np.where(data['day_of_week'] == 4, (COST_TAKER + SLIPPAGE) * 2, 0)
    
    data['net_ret'] = data['strat_ret'] - data['costs']
    return data

def calc_stats(returns):
    # Returns are daily.
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
    print(f"Friday Short")
    print(f"Ret: {tot:.2%}, Sharpe: {sh:.4f}, MDD: {mdd:.2%}")
