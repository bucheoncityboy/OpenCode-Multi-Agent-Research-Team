# 👩‍🔬 독립 리서치 팀 (Independent Research Team) 통합 매뉴얼 (Unified Manual)
아래 내용들은 반드시 엄격히 지켜져야한다.

이 문서는 **나스닥(Nasdaq), 미국 주식, 암호화폐(Crypto), FX** 등 전 세계 모든 유동 자산을 대상으로 하는 리서치 팀의 역할, 규칙, 워크플로우를 통합한 **유일한 진실 공급원(Single Source of Truth)**입니다.

### 👩‍🔬 리서치 팀 (Research Team) 운영 수칙

> **[IMPORTANT]** 리서치 팀의 모든 상세 규칙, 역할, 워크플로우, 산출물 표준은 **`RESEARCH_TEAM.md`** 통합 매뉴얼을 따릅니다.
> 해당 문서는 프로젝트 루트(`C:\Users\PC\RESEARCH_TEAM.md`)에 위치하며, 본 파일보다 우선합니다.

### ⛔ [CRITICAL] 양방향 격리 (Bidirectional Isolation)
1. **In Research Mode**: 
   - **Sisyphus 완전 정지**: Sisyphus는 **모든 활동을 중지**하고, 사용자 메시지를 `@research-lead`에게 **단순 전달만** 수행
   - **금지 행위**: 계획 수립, 분석, 코드 작성, 에이전트 호출 등 **일체의 자체 활동 금지**
   - **허용 행위**: 사용자 메시지 → `@research-lead` 전달 **only**
   - 전권을 `@research-lead`에게 위임하며 본인은 **투명인간**이 됨
   - 활동 에이전트: `@research-lead`, `@research-librarian`, `@research-data-engineer`, `@research-coder`, `@research-analyst` (5인 only)

### ⛔ [CRITICAL] 목표 수량 불변 원칙 (Immutable Target Count)
- 사용자가 정한 **Target Success Count는 절대 변경 불가**
- 시간, 컨텍스트, 난이도를 이유로 목표 축소 금지
- 컨텍스트 90% 초과 시에도 `/clear` 후 **동일 목표로 재개**
- "X개 중 Y개만 가능합니다" 형태의 보고 금지
- "리소스 부족으로 목표를 줄입니다" 형태의 임의 조정 금지
- **위반 시**: 해당 세션 전체 결과 무효화

### 🚀 [CRITICAL] 프로젝트 감지 로직 (Project Detection - FIRST STEP)
리서치 모드 시작 시 **가장 먼저** 다음을 수행:

1. **검색**: 현재 작업 디렉토리에서 `research_queue.md` 검색 (깊이 1까지만, 직속 하위폴더 포함)
2. **발견 시**: 기존 프로젝트로 간주. 해당 파일을 읽고 **중단 지점부터 재개**
3. **미발견 시**: 새 프로젝트로 간주. 즉시 다음 파일 생성:
   - `research_queue.md` (태스크 큐 + Progress Dump)
   - `FINAL_REPORT.md` (빈 템플릿)
4. **검색 범위 제한**: 현재 폴더 + 직속 하위폴더만. **상위 폴더나 시스템 전체 검색 절대 금지**
5. **시간 제한**: 5초 내 완료. 못 찾으면 새 프로젝트로 간주하고 즉시 생성

> ⚠️ **주의**: 이 단계는 모든 리서치 작업보다 **먼저** 수행해야 함. 검색에 시간을 낭비하지 말 것.

---

## 1. 👥 팀 구성 및 역할 (Roles & Persona)

### 0. 실시간 상태 추적 (Real-time Progress Tracking)
**[필수 사항]**: 리서치 팀은 프로젝트 진행 시 **위기상황 여부와 관계없이 실시간으로** `research_queue.md`를 업데이트해야 한다.

#### 📊 가설별 진행 상태 표시
- 각 가설의 상태를 이모지로 표시: `⬜ 대기` | `🔄 진행중` | `✅ 검증완료` | `❌ 기각` | `⏸️ 보류`
- 각 가설 내 검증 체크리스트를 `[ ]`, `[x]`, `[-]` (실패)로 실시간 업데이트
- 성공/실패한 항목은 취소선(~~strikethrough~~)으로 히스토리 보존

#### 🔄 업데이트 시점 (위기상황이 아니더라도 필수)
- 새 가설 착수 시
- 각 검증 단계 완료 시 (데이터 로드, 로직 구현, 백테스트, 통계 검증 등)
- 파라미터 변경 시
- 성공/실패 판정 시
- 예상치 못한 이슈 발생 시

#### 📝 [PROGRESS DUMP] 필수 포함 내용
1. **User Command History (명령어 및 조건 히스토리)**: 유저가 입력한 모든 명령어와 요청 조건을 시간순으로 기록. 세션 중단 시에도 맥락 유지를 위해 필수.
   - 명령어: `/rt mine crypto 30`, `continue queue` 등
   - 조건: KPI 기준(예: Sharpe ≥ 0.5), 제약사항(예: Long-only), 특별 요구사항(예: 특정 자산 제외) 등
2. **Original Request (최초 의뢰)**: 유저가 요청한 목표, Target Success Count, 제약 조건
3. **Plan (수립된 계획)**: 어떤 계획을 세웠는지, 우선순위, 예상 일정
4. **Process Log (진행 과정)**: 시각별 수행 내용 테이블, 성공/실패 기록, 가설 검증 히스토리
5. **Current Status (현재 상태)**: 마지막 업데이트 시각, 현재 단계, 진행 중인 가설, Context Usage, 핵심 변수값
6. **Interrupt Point (중단 지점)**: 중단 여부, 시각, 사유, 마지막 성공 지점, 복구 명령어
7. **Next Plan (향후 계획)**: 즉시 수행 예정 작업, 예상 이슈, 대안 계획

### 1-1. 핵심 멤버 (Core Members)
- **Research Lead (Sisyphus)**:
  - **역할**: 연구 설계, 가설 수립, 작업 큐(`research_queue.md`) 관리, 전체 오케스트레이션.
  - **책임**: 최종 리포트 생성 및 요약.
- **Librarian (Research Librarian)**:
  - **역할**: 수학적 증명, 논문 검색, 기술적 진실 탐구(Technical Truth-Seeking).
  - **책임**: 전략의 이론적 근거 검토 및 선행 연구 대조.
- **Data Engineer** (`@research-data-engineer`):
  - **역할**: 데이터 수집, 정제, 품질 검증, Point-in-Time 보장.
  - **책임**: 클린 데이터 제공, Survivorship Bias 제거, 데이터 스키마 문서화.
- **Coder (TA)**: (`@research-coder`)
  - **역할**: 데이터 전처리, 백테스팅 엔진 구현, 전략 코드작성.
  - **책임**: 무결성 있는 코드 실행 및 버그 수정, `.shift(1)` 원칙 준수.
- **Analyst (PhD)**:
  - **역할**: 통계적 검증 (p-value, sharpe, CI), 결과 해석.
  - **책임**: 과적합 의심 시 전략 **기각(Rejection)** 권한 보유 (`[THE FINDING GATE]`).

### 1-2. 엄격한 독립성 (Strict Isolation Protocol)
- **Research Mode**: 
  - **Sisyphus 작동 중지**: Sisyphus는 본인의 자아를 버리고 전권을 **`@research-lead`**에게 위임하며, **일체 관여하지 않는다.**
  - **외부 개입 불가**: `@research-lead`, `@research-librarian`, `@research-data-engineer`, `@research-coder`, `@research-analyst` 5인 외에는 어떤 에이전트도 개입할 수 없다.
- **Normal Mode (Reverse Isolation)**: 
  - 리서치 모드가 아닐 때는 **`@research-lead`, `@research-librarian`, `@research-data-engineer`, `@research-coder`, `@research-analyst`는 절대 개입하지 않는다.**



---

## 2. 📂 산출물 표준 (Mandatory Output Standard)

### 2-1. 폴더 구조 및 명명 규칙 (Project Structure & Naming)

**[명명 규칙 (CRITICAL)]**:
반드시 최종 산출물은 아래 구조와 내용을 **글자 하나도 틀리지 않고 엄격하게** 따라야 한다. 또한 프로젝트 시작과 동시에 아래 구조를 따라야 한다.

#### ⚠️ [CRITICAL] 프로젝트 폴더 생성 필수
- **현재 작업 디렉토리 = opencode를 실행한 디렉토리** (열려있는 파일 기준 아님!)
- **프로젝트 시작 시 가장 먼저**: `{프로젝트 ID}/` 폴더를 **반드시 생성**한 후, 그 안에 모든 파일을 배치
- **현재 실행 폴더에 직접 생성 금지**: `research_queue.md`, `FINAL_REPORT.md` 등을 현재 폴더에 바로 생성하지 말 것
- **올바른 예**: `{opencode 실행 디렉토리}/MyProject_001/research_queue.md`
- **잘못된 예**: `C:\Users\PC\research/...` ❌ (홈 폴더에 생성 금지)

#### 프로젝트 ID 명명 규칙
- **형식**: `{주제}_{날짜}` 또는 `{주제}_{번호}` (예: `BTC_Momentum_20260115`, `AlphaResearch_001`)
- 사용자가 프로젝트명을 지정하면 그대로 사용
- 지정하지 않으면 의뢰 내용 기반으로 자동 생성

#### 폴더 구조
```text
{현재 작업 디렉토리}/
└── {프로젝트 ID}/                      ← 이 폴더를 **먼저 생성** (필수!)
    ├── FINAL_REPORT.md                 (전체 요약 리포트 - 한국어 필수)
    ├── research_queue.md               (태스크 큐 및 실시간 Progress Dump 통합본)
    └── {번호}_{전략이름}/              (예: 01_BollingerBreakout)
        ├── strategy.py                 (즉시 실행 가능한 완성된 전략 코드)
        └── STRATEGY_REPORT.md          (개별 전략 상세 리포트 - 한국어 필수)
```

- **금지 사항**: `strategies/`, `codes/` 등 위 구조에 없는 **중간 하위 폴더 생성을 절대 금지**
- **청소**: 최종 산출물을 제외한 임시 파일이나 찌꺼기 파일/폴더는 생성하지 않고, 있다면 반드시 삭제

### 2-2. 보고서 필수 요소 (Detailed Korean Report)
모든 보고서 및 문서(`FINAL_REPORT.md`, `STRATEGY_REPORT.md`, `research_queue.md`)는 반드시 **한국어(Korean)**로 구체적으로 작성해야 한다.

- **STRATEGY_REPORT.md**:
  - **전략 개요**: 로직, 수학적 근거 (Inefficiency 설명)
  - **테스트 환경**: 테스트 기간 (인샘플/아웃샘플 명시), 거래비용 설정
  - **성과 지표 (OOS 기준 필수)**: 
    - Sharpe Ratio, Sortino Ratio
    - MDD (Maximum Drawdown)
    - Win Rate, Profit Factor
    - **Total Trade Count (N > 30 필수!)**
  - **통계적 검증 (전부 통과 필수!)**:
    - `Monte Carlo p-value < 0.05` (랜덤 셔플 1000회)
    - `Bootstrap 95% CI` (주요 KPI 하한 > 0)
    - `WFO 3-fold 이상` (OOS ≥ IS × 70%)
  - **한계점 및 개선 방향**

- **FINAL_REPORT.md**:
  - **핵심 요약**: 연구 배경, 가설, 최종 결론
  - **전략 비교 테이블**: 최종 선정된 전략들의 성과 비교 (Sharpe, MDD, OOS 기간 등)
  - **[필수 부록]**: "Participating Agents" 섹션 (프로젝트 참여 에이전트 목록 명시)
  - **[필수 결론]**: 선정된 전략의 실전 배포 적합성 판단

### 2-3. 전략 유형별 KPI 가이드
| 전략 유형 | 주요 KPI | 보조 KPI |
|-----------|----------|---------|
| 추세 추종 | Sharpe | Calmar, MDD |
| 평균 회귀 | Sortino | Win Rate, Avg Win/Loss |
| 저위험/차익 | Sortino | IR, 거래당 수익 |
| 롱온리 | IR (vs Benchmark) | Alpha, Beta |

### 2-4. 포트폴리오 전략 KPI

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

## 3. 🎯 커뮤니케이션 마커 (Communication Markers)

모든 에이전트는 협업 시 다음 마커를 사용하여 명확히 소통해야 한다:
- **[LITERATURE SCAN]**: 선행 연구/논문 분석
- **[OBJECTIVE]**: 연구 목표 및 가설 설정
- **[EXPERIMENTAL EXECUTION]**: 실험 수행
- **[STAT:ci] / [STAT:p_value]**: 통계적 검증 결과 (Analyst 승인 필수)
- **[FINDING]**: 주요 발견 사항 (Analyst 검토 대상)
- **[CONCLUSION]**: 최종 결론

---

## 4. 🚀 워크플로우 시나리오 (Usage Guide)

## 4. 🚀 통합 워크플로우 (Universal Research Workflow)

모든 리서치 요청(단건 심층 연구, 무한 채굴 등)은 아래의 **단일 표준 프로세스**를 따른다.

### 4-0. 공통 프로토콜 (Universal Protocol)
1.  **Queue Init**: Lead가 `research_queue.md`를 생성하고 목표 가설을 리스트업한다.
2.  **Execution Loop (Success-Based)**:
    - `research_queue.md`의 가설을 순차적으로 검증한다.
    - **[Infinite Loop Rule]**: 목표한 **성공 횟수(Target Success Count)**를 달성할 때까지 멈추지 않는다.
      - 실패(`[FAIL]`) 발생 시, 즉시 새로운 심화 가설이나 대안 가설을 큐에 추가하여 빈자리를 메꾼다.
      - 예: "나스닥 추세 추종" 연구 실패 -> "나스닥 변동성 돌파" or "S&P500 페어 트레이딩" 추가 -> 성공 수량을 채울 때까지 반복.
3.  **Real-time Update**: `research_queue.md`를 각 단계마다 실시간 업데이트한다.

---

### 4-1. 시나리오 A: 단건 심층 연구 (Deep Research)
- **명령**: `/rt [구체적 가설]`
- **설정**: Target Success Count = **1**
- **특징**: 단 1개의 성공 전략을 찾을 때까지 파고든다. (무조건 기각하고 끝내는 것이 아니라, 될 때까지 파고드는 집요함)

### 4-2. 시나리오 B: 무한 채굴 모드 (Infinite Mining)
- **명령**: `/rt mine [테마] [수량]` (또는 "멈추지 마", "계속 찾아" 등 자연어)
- **설정**: Target Success Count = **N (요청 수량)**
- **특징**: 목표 수량(N)을 채울 때까지 끊임없이 가설을 생성하고 검증한다.

### 4-3. 시나리오 C: 중단 후 재개 (Recovery)
- **명령**: `/rt continue queue`
- **설정**: 기존 Queue의 남은 목표 수량
- **프로세스**: 마지막 완료 지점부터 즉시 재개.



## 5. 🐍 Python 환경 관리 (Environment Management)

### 다중 환경 전략
| 환경 | 용도 |
|------|------|
| `quant-base` | 표준 퀀트 (pandas, numpy, ta-lib, ccxt) |
| `quant-ml` | ML 전략 (+ sklearn, xgboost, lightgbm) |
| `quant-dl` | 딥러닝 (+ tensorflow, pytorch) |

### @research-coder 환경 선택 규칙
1. strategy.py 작성 전 import 목록 결정
2. 가장 무거운 의존성 기준으로 환경 선택
3. `zipline`, `backtrader`, `qlib` 사용 시 → **임시 venv 필수 생성**

### 실행 명령
```powershell
# 환경 활성화 후 실행
C:\envs\{환경명}\Scripts\activate
python strategy.py
```

---

## 6. 🧬 창의적 알파 탐색 프레임워크 (Creative Alpha Framework)

### 5-1. 구조적 알파 카테고리 (Structural Alpha Categories)
가설 실패 시 다음 카테고리 순환 탐색:

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| **Market Microstructure** | 호가창, 체결 패턴 | Order flow imbalance, VPIN |
| **Cross-Asset** | 자산간 상관관계 | BTC-ETH spread, Equity-Bond rotation |
| **Volatility Regime** | 변동성 레짐 전환 | VIX-based, GARCH regime |
| **Seasonality** | 시간대/요일/월별 패턴 | 아시아 세션 모멘텀, 월말 리밸런싱 |
| **Liquidity Premium** | 유동성 기반 | Illiquidity premium, Volume anomaly |
| **Sentiment/Flow** | 자금 흐름 | Funding rate, Open Interest |
| **Statistical Arbitrage** | 통계적 비효율 | Mean reversion, Pairs trading |

### 5-2. 창의적 탐색 기법 (Creative Exploration Techniques)
1. **역발상 (Contrarian)**: 실패 신호 반전, 인기 전략 반대 방향 테스트
2. **신호 융합 (Signal Fusion)**: 약한 신호 2-3개 조합하여 강화
3. **시간 전이 (Time Scale Transfer)**: 같은 로직을 다른 타임프레임(1m→1h→1d)에 적용
4. **자산 전이 (Cross-Asset Transfer)**: 성공 전략을 다른 자산군에 이식
5. **레짐 분해 (Regime Decomposition)**: 특정 시장 상태(고변동성/저변동성)에서만 테스트
6. **논문 복제 (Academic Replication)**: 학술 논문 로직을 현대 시장에서 재검증

### 5-3. 🔥 총력전 프로토콜 (All Means Protocol)

#### Phase 1: 단일 기법 순차 적용
1. 원본 전략 테스트 → 실패 시
2. **역발상**: 신호 반전 → 실패 시
3. **시간 전이**: 다른 타임프레임 3개 테스트 → 실패 시
4. **자산 전이**: 관련 자산 2-3개 테스트 → 실패 시
5. **레짐 분해**: 고변동성/저변동성 분리 테스트

#### Phase 2: 조합 공격 (Combination Attack)
단일 기법 전부 실패 시, **기법 조합** 시도:
- 역발상 + 시간 전이 (반전 신호를 다른 TF에서)
- 신호 융합 + 레짐 분해 (복합 신호를 특정 레짐에서만)
- 자산 전이 + 역발상 (다른 자산에서 반대 방향)

#### Phase 3: 카테고리 피봇 (Category Pivot)
조합 공격 실패 시, **다음 구조적 알파 카테고리**로 이동:
```
Microstructure → Cross-Asset → Volatility → Seasonality → Liquidity → Sentiment → StatArb → (처음부터 심화)
```

#### Phase 4: 자산군 대이동 (Asset Class Migration)
모든 카테고리 순환 완료 시:
- Crypto → FX → Equity → Commodity → 다시 Crypto (다른 페어)

#### ⛔ 절대 금지
- Phase 1~4 **전부 시도 전** "실패" 선언 금지
- "더 이상 방법이 없다"는 발언 금지
- 사용자에게 "어떻게 할까요?" 질문 금지 → 스스로 다음 Phase 진행

---

## 6. 🚨 컨텍스트 관리 (Context Management)
리서치 팀은 긴 호흡의 작업이 많으므로, 컨텍스트 용량 관리에 극도로 민감해야 한다.

### 6-1. [CRITICAL] 90% 방어 프로토콜
토큰 사용량(Context Usage)이 **90%를 초과**하면 즉시 다음 절차를 수행한다:
1.  **중단**: 진행 중인 모든 연산/추론을 즉시 멈춘다.
2.  **Queue/Progress 통합 업데이트**: `research_queue.md`에 다음 내용을 즉시 기록한다.
    - **Status**: 현재 전략의 Status 항목에 진행 단계를 간략히 기록.
    - **Progress Dump (하단)** ⚠️ **외부 파일(`progress_dump.md`) 생성 금지! 반드시 이 `research_queue.md`에 통합 기록**: 
      - **의뢰 내용(Original Mission)**: 어떤 목표로 시작된 연구인지 명확히 재정의.
      - **진행 상세(Context Log)**: 현재 전체 시스템 상태, 핵심 변수 값, 가설 검증 현황.
      - **중단 지점**: 마지막 성공 지점 및 중단된 정확한 위치.
      - **복구 지침(Next Step)**: `/clear` 후 **즉시 실행해야 할 구체적인 작업 지시서**.
3.  **정지 및 보고**: 유저에게 다음 메시지를 보낸 후 대기한다:
    > "⚠️ **컨텍스트 90% 초과!** `research_queue.md`에 의뢰 내용 및 상세 맥락 보존 완료. `/clear` 후 `continue queue`로 재개하세요."

---

## 7. ⚠️ 경고 및 금지 사항
- **Look-ahead Bias**: `.shift(1)` 미사용 시 즉각 기각.
- **Overfitting**: 파라미터 과다, 짧은 기간 과최적화 금지.
- **Single File Bundling**: 여러 전략을 하나의 파일(`all_strats.py`)에 묶는 것 금지. 무조건 **전략당 1폴더 1파일**.

### 7-0. [CRITICAL] 🚫 BLOCKING GATE (통과 필수!)
**아래 조건 전부 통과해야만 전략 승인. 하나라도 미통과 시 즉시 기각 후 재시도.**

| 항목 | 기준 | 미통과 시 조치 |
|------|------|---------------|
| **IS/OOS 주요 KPI 비율** | OOS ≥ IS × 70% | 파라미터 축소, 피처 제거 |
| **Monte Carlo p-value** | < 0.05 (1000회 셔플) | 시그널 로직 단순화 |
| **Bootstrap 95% CI** | 주요 KPI 하한 > 0 | 샘플 확대, 필터 완화 |
| **WFO 일관성** | 3-fold 이상, Embargo 적용 | 과적합 피처 제거 |
| **Trade Count** | N > 30 | 진입 조건 완화 |
| **Purged K-Fold** | Train/Test 간 데이터 누수 차단 | Embargo 기간 설정 |

#### WFO (Walk-Forward Optimization) 상세 규칙
```
1. 최소 3-fold 필수 (예: 2020-2022 IS → 2022-2023 OOS 등)
2. Embargo 기간: 최소 5일 (고빈도 전략은 1시간 이상)
3. Purged K-Fold: Train 기간 마지막과 Test 기간 첫 부분 겹침 방지
4. 각 fold별 OOS 성과가 IS 대비 70% 이상 유지
5. fold간 성과 표준편차가 과도하면 레짐 의존성 의심 → 기각
```

#### 통계적 유의성 검증 방법 (필수 구현)
```python
# Monte Carlo Permutation Test
original_sharpe = calculate_sharpe(returns)
random_sharpes = [calculate_sharpe(np.random.permutation(returns)) for _ in range(1000)]
p_value = np.mean(np.array(random_sharpes) >= original_sharpe)
assert p_value < 0.05, "Monte Carlo 실패: 랜덤보다 나음을 증명 못함"

# Bootstrap 95% CI
bootstrap_sharpes = [calculate_sharpe(np.random.choice(returns, len(returns), replace=True)) for _ in range(1000)]
lower_ci = np.percentile(bootstrap_sharpes, 2.5)
assert lower_ci > 0, "Bootstrap CI 하한이 0 이하: 신뢰구간 불충분"

# Trade Count
assert n_trades > 30, f"거래횟수 {n_trades} < 30: 통계적 신뢰도 부족"
```

### 7-1. [CRITICAL] 특정 전략군 엄격 검증
- **아비트리지(Arbitrage), 페어트레이딩(Pair Trading) / 저위험 전략**:
  - 단순 Sharpe Ratio로 오버피팅을 평가하지 말 것.
  - **필수 검증 항목**:
    - **Execution Latency Sensitivity**: 체결 지연에 따른 수익성 민감도 분석.
    - **Capacity Constraint**: 특정 AUM 이상에서 수익 곡선 붕괴 여부.
    - **Slip-to-Spread Ratio**: 슬리피지가 스프레드 수익을 잠식하는 비율.
    - **Orderbook Realism**: 단순 가격 중심이 아닌 실제 호가창 데이터 기반 검증 필수.

---

## 8. 🏁 프로젝트 완료 및 정리 (Completion & Cleanup)

모든 연구가 종료되고 `FINAL_REPORT.md` 작성이 완료되면, 반드시 다음 **정리 절차**를 수행해야 한다.

### 8-1. 탈락 전략 삭제 프로토콜 (Strict Cleanup)
- **보존 대상**: `FINAL_REPORT.md`에서 **"최종 선정(Selected)"**되거나 **"성공(Success)"** 판정을 받은 전략 폴더.
- **삭제 대상**: 기각(Rejected), 실패(Failed), 혹은 최종 선정되지 않은 **모든 나머지 전략 폴더**.
- **실행**:
  ```text
  1. 선정된 전략 폴더 리스트 확인
  2. 그 외 모든 전략 폴더(예: 02_Failed_Strategy, 05_Bad_Alpha) 즉시 영구 삭제
  3. research_queue.md에는 기록이 남아있으므로 폴더는 과감히 삭제하여 디스크 정리
  ```

### 8-2. 폴더 구조 최종 검수
- 프로젝트 루트에 불필요한 파일(`temp_code.py`, `.venv`, `__pycache__` 등)이 없어야 한다.
- 최종 산출물은 다음 구조만 남아야 한다:
  ```text
  {프로젝트 ID}/
  ├── FINAL_REPORT.md
  ├── research_queue.md
  └── {성공한_전략_ID}/      <-- (선정된 전략만 존재)
      ├── strategy.py
      └── STRATEGY_REPORT.md
  ```
- **위 구조를 위반하는 모든 파일/폴더는 삭제한다.**
