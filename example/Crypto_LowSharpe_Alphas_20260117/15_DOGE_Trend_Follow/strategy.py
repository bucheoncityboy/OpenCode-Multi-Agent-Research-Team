import pandas as pd
import numpy as np
import os

DATA_PATH = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/DOGEUSDT_15m_2024-01-01_2024-12-31.csv"
COST_TAKER = 0.0004
SLIPPAGE = 0.0001
EMA_PERIOD = 50

def load_data(path):
    if not os.path.exists(path):
        # Try finding DOGE file
        # List dir to check
        pass
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    return df

def run_strategy(df):
    data = df.copy()
    ohlc = {'open':'first', 'high':'max', 'low':'min', 'close':'last'}
    df_1h = data.resample('1h').agg(ohlc).dropna()
    
    df_1h['ema'] = df_1h['close'].ewm(span=EMA_PERIOD).mean()
    
    # Logic: Long if Price > EMA
    df_1h['signal'] = np.where(df_1h['close'] > df_1h['ema'], 1, -1)
    
    df_1h['position'] = df_1h['signal'].shift(1).fillna(0)
    
    df_1h['ret'] = df_1h['close'].pct_change()
    df_1h['strat_ret'] = df_1h['position'] * df_1h['ret']
    
    df_1h['trades'] = df_1h['position'].diff().abs().fillna(0)
    df_1h['costs'] = df_1h['trades'] * (COST_TAKER + SLIPPAGE)
    df_1h['net_ret'] = df_1h['strat_ret'] - df_1h['costs']
    return df_1h

def calc_stats(returns):
    n = 365 * 24
    if returns.std() == 0: return 0, 0, 0
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n)
    cum = (1+returns).cumprod()
    tot = cum.iloc[-1]-1
    mdd = ((cum - cum.cummax())/cum.cummax()).min()
    return tot, sharpe, mdd

if __name__ == "__main__":
    try:
        df = load_data(DATA_PATH)
        res = run_strategy(df)
        tot, sh, mdd = calc_stats(res['net_ret'])
        print(f"DOGE Trend Follow")
        print(f"Ret: {tot:.2%}, Sharpe: {sh:.4f}, MDD: {mdd:.2%}")
    except Exception as e:
        print(f"Error: {e}")
