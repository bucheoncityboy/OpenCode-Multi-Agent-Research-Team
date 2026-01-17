import pandas as pd
import numpy as np
import os

# -----------------------------------------------------------------------------
# 1. Configuration
# -----------------------------------------------------------------------------
DATA_PATH = "C:/Users/PC/Desktop/Quant/STRATEGY/11_funding_carry/data/binance_funding_rates.csv"
SYMBOL = "BTC/USDT"
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
COST_TAKER = 0.0004
SLIPPAGE = 0.0001

# Parameters
ENTRY_THRESHOLD_APR = 0.10  # 10%
EXIT_THRESHOLD_APR = 0.05   # 5%

# -----------------------------------------------------------------------------
# 2. Data Loading
# -----------------------------------------------------------------------------
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data not found: {path}")
    df = pd.read_csv(path)
    # Check cols: usually timestamp, symbol, fundingRate
    df.columns = [c.lower() for c in df.columns]
    
    # Filter Symbol
    if 'symbol' in df.columns:
        print(f"Available symbols: {df['symbol'].unique()[:5]}")
        df = df[df['symbol'] == SYMBOL].copy()
        print(f"Rows after filter: {len(df)}")
    
    if 'datetime' in df.columns:
        df['timestamp'] = pd.to_datetime(df['datetime'])
        df.set_index('timestamp', inplace=True)
    elif 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
    df.sort_index(inplace=True)
    return df

# -----------------------------------------------------------------------------
# 3. Strategy Logic
# -----------------------------------------------------------------------------
def run_strategy(df):
    data = df.copy()
    
    # Funding Rate is usually per 8h interval
    # Calculate APR
    data['apr'] = data['fundingrate'] * 3 * 365
    
    # Logic:
    # Enter (Position=1) if APR > Entry
    # Exit (Position=0) if APR < Exit
    
    data['signal'] = np.nan
    data.loc[data['apr'] > ENTRY_THRESHOLD_APR, 'signal'] = 1
    data.loc[data['apr'] < EXIT_THRESHOLD_APR, 'signal'] = 0
    
    data['position'] = data['signal'].ffill().fillna(0)
    
    # Returns (Carry)
    # If Position=1, we earn Funding Rate (at the end of 8h).
    # Funding is paid at timestamp.
    # So if we hold at T-1, we receive Funding at T.
    # Return = Position(T-1) * FundingRate(T)
    # Note: Short Perp receives positive funding if rate is positive.
    # Long Spot pays nothing.
    # Net = Funding Rate.
    
    data['strat_ret'] = data['position'].shift(1) * data['fundingrate']
    
    # Costs
    # We pay trading fees on Entry/Exit of the HEDGE.
    # Spot Long + Perp Short = 2 legs.
    # Cost = 2 * (Taker + Slippage)
    
    data['trades'] = data['position'].diff().abs().fillna(0)
    data['costs'] = data['trades'] * (COST_TAKER + SLIPPAGE) * 2
    
    data['net_ret'] = data['strat_ret'] - data['costs']
    
    return data

def calc_stats(returns):
    # 8H periods = 3 per day
    n = 365 * 3
    if returns.std() == 0: return 0, 0, 0
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n)
    cum = (1+returns).cumprod()
    tot = cum.iloc[-1]-1
    mdd = ((cum - cum.cummax())/cum.cummax()).min()
    return tot, sharpe, mdd

if __name__ == "__main__":
    try:
        df = load_data(DATA_PATH)
        df = df[START_DATE:END_DATE]
        
        # Resample to ensure 8H grid?
        # Usually funding is every 8h.
        
        res = run_strategy(df)
        tot, sh, mdd = calc_stats(res['net_ret'])
        
        print(f"Funding Rate Carry ({SYMBOL})")
        print(f"Ret: {tot:.2%}, Sharpe: {sh:.4f}, MDD: {mdd:.2%}")
        
    except Exception as e:
        print(f"Error: {e}")
