# 🧬 퀀트 코드 템플릿

> ⚠️ **[MANDATORY]** 코드 작성 전 이 템플릿을 **반드시 먼저** 참조할 것!

---

## 1. 기본 임포트 & quant_utils

```python
import sys
sys.path.insert(0, r'C:\Users\PC')
from quant_utils import quick_validate
```

---

## 2. 통계적 검증

```python
import numpy as np

def calculate_sharpe(returns, risk_free=0):
    excess = returns - risk_free
    return np.sqrt(252) * excess.mean() / excess.std()

def statistical_validation(returns, n_trades, is_sharpe, oos_sharpe):
    # Monte Carlo
    original = calculate_sharpe(returns)
    p_value = np.mean([calculate_sharpe(np.random.permutation(returns)) >= original 
                       for _ in range(1000)])
    assert p_value < 0.05, f"MC 실패: p={p_value:.3f}"
    
    # Bootstrap 95% CI
    lower_ci = np.percentile([calculate_sharpe(np.random.choice(returns, len(returns), replace=True)) 
                              for _ in range(1000)], 2.5)
    assert lower_ci > 0, f"CI 하한 {lower_ci:.3f} <= 0"
    
    # Trade Count & OOS/IS
    assert n_trades > 30, f"N={n_trades} < 30"
    ratio = oos_sharpe / is_sharpe if is_sharpe > 0 else 0
    assert ratio >= 0.7, f"OOS/IS={ratio:.1%} < 70%"
    
    return True
```

---

## 3. WFO 설정

```python
FOLDS = [
    ('2020-01-01', '2021-12-31', '2022-01-01', '2022-06-30'),
    ('2021-01-01', '2022-12-31', '2023-01-01', '2023-06-30'),
    ('2022-01-01', '2023-12-31', '2024-01-01', '2024-06-30'),
]
EMBARGO_DAYS = 5
```

---

## 4. quick_validate 사용

```python
passed, results = quick_validate(
    df=df, returns=returns, signal_col='signal',
    feature_cols=[...], is_sharpe=is_sharpe,
    oos_sharpe=oos_sharpe, n_params=n_params
)
if not passed: print('❌ 실패 → 수정 후 재시도')
```

---

## 5. 피처 규칙 (.shift 필수!)

```python
# ⚠️ 모든 피처에 .shift(1) 필수!
df['sma'] = df['close'].rolling(20).mean().shift(1)
df['rsi'] = ta.rsi(df['close'], 14).shift(1)
df['vol'] = df['returns'].rolling(20).std().shift(1)
```

---

## 6. 거래비용

```python
MAKER_FEE = 0.0002  # 2bp
TAKER_FEE = 0.0005  # 5bp
```

---

## 7. Purged K-Fold

```python
from sklearn.model_selection import TimeSeriesSplit

def purged_kfold(df, n_splits=3, embargo=5):
    tscv = TimeSeriesSplit(n_splits=n_splits, gap=embargo)
    for train_idx, test_idx in tscv.split(df):
        yield train_idx[:-embargo], test_idx
```

---

## 🔐 참조 검증 코드
**이 문서를 읽었다면 코드 작성 시작 시 반드시 출력**: `[QT-v1-OK]`
