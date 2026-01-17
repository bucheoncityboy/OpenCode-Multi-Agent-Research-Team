import pandas as pd
import numpy as np
import os

# -----------------------------------------------------------------------------
# 1. Configuration
# -----------------------------------------------------------------------------
DATA_PATH = "C:/Users/PC/Desktop/Quant/boll/sniper/data_cache/BTCUSDT_15m_2024-01-01_2025-12-31.csv"
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
COST_TAKER = 0.0004
SLIPPAGE = 0.0001

# Strategy Parameters
EMA_FAST = 20
EMA_SLOW = 50
ATR_PERIOD = 14
RISK_FACTOR = 0.01  # Target Risk per trade (not fully used in simple backtest, used for sizing)

# -----------------------------------------------------------------------------
# 2. Data Loading (Reused)
# -----------------------------------------------------------------------------
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data not found: {path}")
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
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
    
    # Resample to 1H for Trend Signals (More robust than 15m)
    # We will trade on 1H signals
    ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close':'last', 'volume':'sum'}
    df_1h = data.resample('1h').agg(ohlc_dict).dropna()
    
    # Indicators
    df_1h['ema_fast'] = df_1h['close'].ewm(span=EMA_FAST).mean()
    df_1h['ema_slow'] = df_1h['close'].ewm(span=EMA_SLOW).mean()
    
    # ATR for Volatility Scaling
    df_1h['tr'] = np.maximum(
        df_1h['high'] - df_1h['low'],
        np.maximum(
            abs(df_1h['high'] - df_1h['close'].shift(1)),
            abs(df_1h['low'] - df_1h['close'].shift(1))
        )
    )
    df_1h['atr'] = df_1h['tr'].rolling(ATR_PERIOD).mean()
    
    # Signal: Golden Cross
    # Shift(1) to avoid lookahead: Signal calculated at Close of T, Enter at Open of T+1
    df_1h['signal_raw'] = np.where(df_1h['ema_fast'] > df_1h['ema_slow'], 1, -1)
    df_1h['signal'] = df_1h['signal_raw'].shift(1)
    
    # Position Sizing: Inverse Volatility
    # Target Position = (Constant / ATR)
    # Normalized: If ATR is high, position is small.
    # Let's target strictly inverse: 1 / ATR
    # To make it realistic, let's normalize so avg position is 1.0
    avg_atr = df_1h['atr'].mean()
    df_1h['position_size'] = (avg_atr / df_1h['atr']).clip(0.1, 3.0) # Cap leverage at 3x, min 0.1x
    
    df_1h['position'] = df_1h['signal'] * df_1h['position_size']
    
    # Returns
    df_1h['price_return'] = df_1h['close'].pct_change()
    df_1h['strategy_returns'] = df_1h['position'].shift(1) * df_1h['price_return']
    
    # Costs
    # Change in position * Cost
    df_1h['pos_change'] = df_1h['position'].diff().abs().fillna(0)
    df_1h['costs'] = df_1h['pos_change'] * (COST_TAKER + SLIPPAGE)
    
    df_1h['net_returns'] = df_1h['strategy_returns'] - df_1h['costs']
    
    return df_1h

# -----------------------------------------------------------------------------
# 4. Metrics
# -----------------------------------------------------------------------------
def calculate_metrics(returns):
    n_periods = 365 * 24 # 1H data
    sharpe = (returns.mean() / returns.std()) * np.sqrt(n_periods) if returns.std() != 0 else 0
    
    cum_ret = (1 + returns).cumprod()
    total_ret = cum_ret.iloc[-1] - 1
    
    rolling_max = cum_ret.cummax()
    mdd = ((cum_ret - rolling_max) / rolling_max).min()
    
    return {"Total Return": total_ret, "Sharpe": sharpe, "MDD": mdd}

if __name__ == "__main__":
    try:
        df = load_data(DATA_PATH)
        df = df[START_DATE:END_DATE]
        result = run_strategy(df)
        metrics = calculate_metrics(result['net_returns'])
        
        print("-" * 30)
        print("Vol-Scaled Trend Strategy")
        print("-" * 30)
        print(f"Total Return: {metrics['Total Return']:.2%}")
        print(f"Sharpe Ratio: {metrics['Sharpe']:.4f}")
        print(f"Max Drawdown: {metrics['MDD']:.2%}")
        
    except Exception as e:
        print(f"Error: {e}")
