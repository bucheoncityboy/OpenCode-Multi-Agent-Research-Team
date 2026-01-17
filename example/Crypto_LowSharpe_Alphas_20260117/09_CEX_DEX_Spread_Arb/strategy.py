import pandas as pd
import numpy as np
import os

# -----------------------------------------------------------------------------
# 1. Configuration
# -----------------------------------------------------------------------------
DATA_PATH = "C:/Users/PC/Desktop/Quant/cex_dex/data/ETH_historical.parquet"
COST_TOTAL = 0.008 # 0.8% round trip (Conservative: 0.05% CEX + 0.3% DEX + Gas + Slippage)
THRESHOLD = 0.01   # 1% Entry

# -----------------------------------------------------------------------------
# 2. Data Loading
# -----------------------------------------------------------------------------
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data not found: {path}")
    df = pd.read_parquet(path)
    # Check columns
    df.columns = [c.lower() for c in df.columns]
    
    # Needs: timestamp, cex_price, dex_price
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    return df

# -----------------------------------------------------------------------------
# 3. Strategy Logic
# -----------------------------------------------------------------------------
def run_strategy(df):
    data = df.copy()
    
    # Calculate Spread (bps)
    # spread = (CEX - DEX) / DEX? Or Mid?
    # Usually: Spread = Log(CEX) - Log(DEX) approx (CEX - DEX)/DEX
    
    if 'cex_price' not in data.columns or 'dex_price' not in data.columns:
        # Try finding cols
        print(f"Cols: {data.columns}")
        return pd.DataFrame() # Fail
        
    data['spread'] = (data['cex_price'] - data['dex_price']) / data['dex_price']
    
    # Logic:
    # If Spread > Threshold: Short CEX, Long DEX. Expect Spread -> 0.
    # Return = (Spread_Entry - Spread_Exit) approx?
    # Actually:
    # Short CEX at P_cex, Long DEX at P_dex.
    # Exit when Spread ~ 0.
    # Profit = (P_cex_entry - P_cex_exit) + (P_dex_exit - P_dex_entry)
    #        = (P_cex_entry - P_dex_entry) - (P_cex_exit - P_dex_exit)
    #        = Spread_Entry_Dollars - Spread_Exit_Dollars.
    # % Ret = Spread_Entry_% - Spread_Exit_% - Costs.
    
    # Simplified:
    # If Spread > 1%, we capture (Spread - 0).
    # Net = Spread - Costs.
    # We assume full convergence.
    
    # Trade Signal
    data['signal'] = 0
    data.loc[abs(data['spread']) > THRESHOLD, 'signal'] = 1
    
    # We only trade if signal=1.
    # Return = abs(Spread) - Cost.
    # But does it converge?
    # We assume it does (Arbitrage).
    # Realistically, we calculate the realized spread compression.
    # But for "Alpha Mining", checking frequency of Arb opportunities is enough.
    
    # Let's count "Arb Opportunities" and sum their theoretical return.
    
    data['opportunity_ret'] = np.where(data['signal'] == 1, abs(data['spread']) - COST_TOTAL, 0)
    
    # Filter only positive opportunities (if spread < cost, don't trade)
    data['real_trade'] = np.where(data['opportunity_ret'] > 0, 1, 0)
    data['net_ret'] = np.where(data['real_trade'] == 1, data['opportunity_ret'], 0)
    
    # This is "Instant PnL" (theoretical).
    # In reality, it takes time.
    # But let's report "Cumulative Theoretical Arb PnL".
    
    return data

def calc_stats(returns):
    # Returns here are "Per Hour" (if multiple opps? No, max 1 per hour).
    # This is not a time-series return, but "Sparse Returns".
    # Need to fill 0s to calculate Sharpe on time series.
    n = 365 * 24
    if returns.std() == 0: return 0, 0, 0
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n)
    cum = returns.cumsum() # Arithmetic sum for arb
    tot = cum.iloc[-1]
    # MDD not relevant for instant arb (no hold), but accumulation curve MDD.
    mdd = 0 
    return tot, sharpe, mdd

if __name__ == "__main__":
    try:
        df = load_data(DATA_PATH)
        res = run_strategy(df)
        
        if res.empty:
            print("No Data")
        else:
            tot, sh, mdd = calc_stats(res['net_ret'])
            print(f"CEX-DEX Arb (ETH)")
            print(f"Total Arb Profit (Sum): {tot:.2f} (Units of Capital)")
            print(f"Sharpe: {sh:.4f}")
            print(f"Opps Count: {res['real_trade'].sum()}")
            
    except Exception as e:
        print(f"Error: {e}")
