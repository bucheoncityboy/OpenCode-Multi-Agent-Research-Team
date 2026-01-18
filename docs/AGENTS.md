# 퀀트 리서처/개발자 전역 규칙

## 언어
- **모든 답변과 사고 과정은 한국어로 작성**

## 환경
- Python 3.11+
- pandas, numpy, scipy 기반
- 타입 힌트 필수

---

## 🚨 컨텍스트 관리 (최우선 순위)

매 답변마다 토큰 사용량(Context Usage)을 확인하고, **90%를 초과하면 즉시:**
1. 진행 중인 작업 중단
2. 현재까지의 진행 상황, 변수 상태, 다음 작업을 저장:
   - **리서치 모드**: 프로젝트 폴더 내 `research_queue.md`에 통합 기록 (외부 파일 생성 금지)
   - **노말 모드**: `progress_dump.md`에 저장
3. 다음 메시지 출력 후 정지:
   > "⚠️ **컨텍스트 90% 초과!** 상태 저장 완료. `/clear` 후 이어서 진행하세요."

---

## 🚨 핵심 원칙 - 3대 배제 (엄격히 배제!)

### 1. 오버피팅 엄격히 배제 ❌
- 파라미터 과다 튜닝 금지 (파라미터 수 < 데이터 포인트 / 10)
- 인샘플 과최적화 금지
- 하드코딩된 매직 넘버 금지
- Walk-forward validation 필수

### 2. 데이터 누수 엄격히 배제 ❌
- Look-ahead bias 절대 금지
- 시점 기준 엄격 준수 (point-in-time)
- `.shift()` 사용 철저
- 피처 생성 시 미래 정보 유출 점검

### 3. 편향 엄격히 배제 ❌
- **Look-ahead bias (미래 편향)** 절대 금지
- Survivorship bias 제거
- Selection bias 제거
- Confirmation bias 경계

---

## 📊 백테스트 기준

### 거래비용 (Asset-Specific Fees)
모든 백테스트는 대상 시장의 실제 비용을 엄격히 반영해야 한다:

| 자산군 | Maker | Taker | 슬리피지/기타 |
|--------|-------|-------|---------------|
| **Crypto (Binance)** | 0.02% | 0.04% | 유동성 기반 별도 계산 |
| **US Stocks (Nasdaq)** | $0.00 | $0.00 | $0.005/share (수수료) + Spread |
| **FX (Daily)** | 0.0 bp | 0.0 bp | Spread (자산별 상이) |
| **Futures** | 0.01% | 0.02% | 틱 사이즈 기반 슬리피지 |

### 검증 방법
- 인샘플/아웃샘플 분리 필수 (70/30 또는 Walk-forward)
- 인샘플 Sharpe > 3.0 → 과적합 의심
- 아웃샘플 성과 저하 > 30% → 과적합 경고

### 성과 지표 (필수) 결과 도출시 출력할 것 
| 지표 | 기준 |
|------|------|
| Sharpe Ratio | 연율화, rf=0 |
| MDD | 최대 낙폭 |
| Win Rate | 승률 |
| Profit Factor | > 1.5 권장 |
| Trade Count | N > 30 필수 |

### 통계적 유의성 (필수) 결과 도출시 성과지표 밑에 출력할 것 
| 방법 | 기준 |
|------|------|
| **Monte Carlo Permutation** | p-value < 0.05 (랜덤 셔플 1000회 대비) |
| **Bootstrap 95% CI** | Sharpe 하한 > 0 |
| **WFO OOS 유지율** | 아웃샘플 Sharpe ≥ 인샘플 × 70% |

### 📝 리포트 작성 규칙 (CRITICAL)
| 항목 | 규칙 |
|------|------|
| **언어** | 모든 리포트(FINAL_REPORT, STRATEGY_REPORT)는 **반드시 한글**로 작성 |
| **테스트 기간** | 인샘플/아웃샘플 기간 **필수 명시** (YYYY-MM-DD ~ YYYY-MM-DD) |
| **성과 지표** | **OOS(아웃샘플) 결과만 표시**, IS 수치는 리포트에 미포함 |

### 📈 전략 유형별 KPI 가이드
| 전략 유형 | 주요 KPI | 보조 KPI |
|-----------|----------|---------|
| 추세 추종 | Sharpe | Calmar, MDD |
| 평균 회귀 | Sortino | Win Rate, Avg Win/Loss |
| 저위험/차익 | Sortino | IR, 거래당 수익 |
| 롱온리 | IR (vs Benchmark) | Alpha, Beta |

### 📐 KPI 등급 기준표 (Sharpe 기준 → 자동 변환)
사용자가 "Sharpe ≥ X"로만 기준을 제시하면, 전략 유형에 따라 아래 등급의 해당 KPI로 자동 변환:

| 등급 | Sharpe | Sortino | IR | 적용 조건 |
|------|--------|---------|-----|----------|
| 최소 | ≥ 0.5 | ≥ 0.7 | ≥ 0.3 | 사용자 기준 < 1.0 |
| 양호 | ≥ 1.0 | ≥ 1.5 | ≥ 0.5 | 사용자 기준 ≥ 1.0 |
| 우수 | ≥ 2.0 | ≥ 2.5 | ≥ 1.0 | 사용자 기준 ≥ 2.0 |

**적용 규칙:**
1. 사용자가 "Sharpe ≥ X"로만 기준 제시 시 → 등급 매핑
2. 전략 유형에 맞는 해당 등급의 KPI 기준 자동 적용
3. 사용자가 개별 KPI를 명시하면 그대로 사용 (변환 안 함)

**예시:** 사용자가 "Sharpe ≥ 2.0" 명령 → 우수 등급 적용
- 추세 추종: Sharpe ≥ 2.0
- 평균 회귀: Sortino ≥ 2.5
- 저위험/차익: Sortino ≥ 2.5
- 롱온리: IR ≥ 1.0

### 📦 포트폴리오 전략 KPI

#### 일반 포트폴리오 (주식/FX/혼합)
| 지표 | 기준 |
|------|------|
| 평균 상관계수 | < 0.3 |
| 롤링 최대 상관 (60일) | < 0.7 |
| 위기 기간 상관 | < 0.6 |

#### 크립토 전용 포트폴리오
| 지표 | 기준 |
|------|------|
| 평균 상관계수 | < 0.5 |
| 롤링 최대 상관 (60일) | < 0.85 |
| 위기 기간 상관 | < 0.8 |

#### 공통 기준
| 지표 | 기준 |
|------|------|
| Portfolio Sharpe | > 개별 전략 평균 Sharpe |
| 분산효과 비율 | > 1.2 |
| 최대 리스크 집중도 | 단일 전략 < 40% |
| Portfolio MDD | < 개별 MDD 평균 |


---

## 💻 코드 스타일

### 필수 규칙
- **쓸데없는 주석 금지** (코드로 설명되는 내용은 주석 X)
- 벡터화 연산 우선 (for 루프 지양)
- 인덱스 정렬 철저 (`df.sort_index()`)
- 결측치 처리 명시
- 랜덤 시드 설정

```python
def calculate_returns(prices: pd.Series, periods: int = 1) -> pd.Series:
    return np.log(prices / prices.shift(periods))
```

---

## 📁 프로젝트 구조 권장

```
project/
├── data/
├── features/
├── models/
├── backtest/
├── analysis/
├── reports/
project/
├── data/
├── features/
├── models/
├── backtest/
├── analysis/
├── reports/
├── research/           <-- Research Mode Base
│   └── results/        <-- Automated Results
│       └── YYYYMMDD_HHMMSS/
│           ├── FINAL_REPORT.md
│           ├── Strategy_A/
│           │   ├── code.py (Archived)
│           │   └── STRATEGY_REPORT.md
│           └── Strategy_B/
└── tests/

```

---

## ⚠️ 경고 신호

즉시 경고 발생 조건:
- Sharpe > 3.0 (비현실적)
- MDD < 5% with Sharpe > 2.0 (의심)
- 인샘플/아웃샘플 성과 차이 > 50%
- 급격한 equity curve 점프

---

## 🚫 BLOCKING GATE (통과 전 진행 금지)

다음 조건 **모두 충족** 전까지 최종 보고서 생성 금지:

| 검증 항목 | 기준 | 미통과 시 조치 |
|-----------|------|----------------|
| IS/OOS Sharpe 비율 | OOS ≥ IS × 70% | 파라미터 축소 후 재검증 |
| Monte Carlo p-value | < 0.05 (1000회 셔플) | 시그널 로직 재검토 |
| Bootstrap 95% CI | Sharpe 하한 > 0 | 신뢰구간 불충분, 샘플 확대 |
| Walk-Forward Consistency | 3-fold 이상 일관성 | 과적합 의심, 피처 제거 |
| Trade Count | N > 30 | 필터 조건 완화 |

### 미통과 시 자동 재시도 루프
```
검증 실패 → 원인 분석 → 해당 요소 배제/수정 → 재백테스트 → 재검증
(최대 3회 반복, 이후 사용자 개입 요청)
```

---

## 📊 베이스라인 비교 (필수)

모든 전략은 아래 베이스라인 대비 우위 입증 필수:

| 베이스라인 | 비교 지표 | 기준 |
|------------|-----------|------|
| 랜덤 시그널 (1000회 셔플) | p-value | < 0.05 |
| Buy & Hold | Information Ratio (IR) | > 0 |
| 단순 모멘텀/역추세 | 초과 Sharpe | > 0.2 |

---

## 🔒 시계열 CV 필수 요구사항

시계열 데이터 누수 방지를 위한 필수 설정:

- **Purged K-Fold**: 훈련/검증 사이 gap 기간 설정
- **Embargo**: 훈련 종료 ~ 검증 시작 사이 버퍼 (최소 1일)
- **purge_length**: max(모든 피처의 lookback periods)
- **Rolling WFO**: 최소 3-fold 필수, 단일 split 결과 불신

---

## 🐍 Python 환경 관리 (Environment Management)

### 다중 환경 전략 (Multi-Tier Environments)

| 환경 | 경로 | 용도 | 패키지 |
|------|------|------|--------|
| **quant-base** | `C:\envs\quant-base` | 표준 퀀트 리서치 | pandas, numpy, scipy, ta-lib, ccxt |
| **quant-ml** | `C:\envs\quant-ml` | ML 기반 전략 | + scikit-learn, xgboost, lightgbm |
| **quant-dl** | `C:\envs\quant-dl` | 딥러닝 전략 | + tensorflow, pytorch, keras |

### 🔍 자동 환경 선택 규칙
코드에서 다음 import 발견 시 해당 환경 활성화:
```
기본 (quant-base): pandas, numpy, scipy, matplotlib, ta-lib, ccxt
ML (quant-ml): sklearn, xgboost, lightgbm, catboost
DL (quant-dl): tensorflow, torch, keras, transformers
특수 (임시 venv): zipline, backtrader, qlib (충돌 위험)
```

### 📋 실행 프로토콜
1. **코드 분석**: strategy.py의 import 문 스캔
2. **환경 결정**: 가장 무거운 의존성 기준으로 선택
3. **활성화 & 실행**:
   ```powershell
   # 예: ML 전략
   C:\envs\quant-ml\Scripts\activate
   python strategy.py
   ```
4. **requirements.txt 생성**: 각 프로젝트에 버전 기록

### ⚠️ 임시 venv 생성 조건
다음 패키지 사용 시 **프로젝트 전용 임시 환경** 생성:
- `zipline`, `zipline-reloaded`
- `backtrader`
- `qlib`
- 기타 버전 고정이 필요한 레거시 라이브러리

```powershell
# 임시 venv 생성
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# ... 작업 완료 후 ...
rmdir /s /q .venv
```

---

## 🧬 창의적 알파 탐색 (Creative Alpha Exploration)

전략 개발 실패 또는 검증 미통과 시, 다음 창의적 접근법을 순차적으로 시도:

### 구조적 알파 카테고리
| 카테고리 | 예시 |
|----------|------|
| Market Microstructure | Order flow, VPIN, Spread dynamics |
| Cross-Asset | 자산간 스프레드, Rotation |
| Volatility Regime | VIX 기반, GARCH 레짐 |
| Seasonality | 시간대/요일/월별 패턴 |
| Liquidity Premium | 거래량 이상, 유동성 프리미엄 |
| Sentiment/Flow | Funding rate, OI 변화 |

### 🔥 총력전 프로토콜 (All Means Protocol)

#### 실패 시 순차 적용
1. **역발상**: 신호 반전 테스트
2. **신호 융합**: 약한 신호 2-3개 조합
3. **시간 전이**: 다른 타임프레임 테스트 (1m/5m/1h/4h/1d)
4. **자산 전이**: 관련 자산 2-3개에 동일 로직 적용
5. **레짐 분해**: 고변동성/저변동성 분리 테스트

#### 조합 공격 (단일 기법 전부 실패 시)
- 역발상 + 시간 전이
- 신호 융합 + 레짐 분해
- 자산 전이 + 역발상

#### 카테고리 피봇 (조합도 실패 시)
다음 구조적 알파 카테고리로 이동 후 Phase 1부터 재시도

> **적용 시점**: @backtester/@debugger 검증 실패 후 @oracle/@coder가 재설계 시
> **절대 금지**: 위 기법 전부 시도 전 "실패" 선언

---

## 🔑 Research Mode 활성화 조건 (Trigger Condition)

Research Mode는 **오직 다음 조건에서만** 활성화된다:
1. 사용자가 명시적으로 `/rt` 명령어를 호출했을 때
2. 사용자가 "리서치 모드 시작", "Research Mode" 등 명시적 활성화 키워드를 사용했을 때

> [!CAUTION]
> **다음 조건들은 Research Mode를 활성화하지 않는다:**
> - `research/` 폴더 내 파일 작업
> - `research_queue.md` 존재
> - `strategy.py` 파일 수정
> - 백테스트 관련 작업

---

## 👩‍🔬 리서치 팀 (Research Team) 운영 수칙

> **[IMPORTANT]** 리서치 팀의 모든 상세 규칙, 역할, 워크플로우, 산출물 표준은 **`RESEARCH_TEAM.md`** 통합 매뉴얼을 따릅니다.
> 해당 문서는 프로젝트 루트(`C:\Users\PC\RESEARCH_TEAM.md`)에 위치하며, 본 파일보다 우선합니다.

### ⛔ [CRITICAL] 양방향 격리 (Bidirectional Isolation)
1. **In Research Mode**: 
   - **Sisyphus 완전 정지**: Sisyphus는 **모든 활동을 중지**하고, 사용자 메시지를 `@research-lead`에게 **단순 전달만** 수행
   - **금지 행위**: 계획 수립, 분석, 코드 작성, 에이전트 호출 등 **일체의 자체 활동 금지**
   - **허용 행위**: 사용자 메시지 → `@research-lead` 전달 **only**
   - 전권을 `@research-lead`에게 위임하며 본인은 **투명인간**이 됨
   - 활동 에이전트: `@research-lead`, `@research-librarian`, `@research-data-engineer`, `@research-coder`, `@research-analyst` (5인 only)
2. **In Normal Mode**: 위 5명의 리서치 전용 에이전트(`@research-*`)는 **절대 개입 엄금**. 특히 `@research-coder`와 일반 Coder 혼동 금지.




