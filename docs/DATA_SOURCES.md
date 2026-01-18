# 📊 무료 데이터 소스 가이드 (Free Tier Data Sources)

> ⚠️ **[MANDATORY]** Data Engineer는 데이터 수집 전 **반드시** 이 문서를 참조할 것!

---

## 🔑 API 키 필요 여부 요약

> 💡 아래는 **예시 목록**이며, 전략에 따라 **자유롭게 선택**하여 사용할 것. 제한하지 말 것!

### ✅ API 키 불필요 (바로 사용 가능)
| 소스 | 데이터 유형 |
|------|-------------|
| **yfinance** | 주식 OHLCV, 재무제표 |
| **CCXT** | 암호화폐 OHLCV (거래소 공개 API) |
| **Binance/Bybit API** | Funding Rate, OI, OHLCV |
| **CoinGecko** | 마켓캡, 볼륨 |
| **Fear & Greed** | 시장 심리 지수 |
| **Google Trends** | 검색 트렌드 |
| **DefiLlama** | DeFi TVL, DEX 볼륨 |
| **Dune Analytics** | 온체인 (공개 쿼리) |
| **CoinPaprika** | 마켓 데이터 |
| **DEX Screener** | DEX 실시간 가격, 신규 페어 |
| **GeckoTerminal** | DEX 유동성, 트렌딩 풀 |
| **0x / 1inch API** | DEX 집계, 스왑 견적 |
| **Uniswap Subgraph** | 풀, 스왑, 유동성 이벤트 |

### 🔐 무료 API 키 필요 (가입만 하면 됨)
| 소스 | 가입 URL | 한도 |
|------|----------|------|
| **Alpha Vantage** | alphavantage.co | 25 req/day |
| **Finnhub** | finnhub.io | 60 req/min |
| **FRED** | fred.stlouisfed.org | 무제한 |
| **CryptoCompare** | cryptocompare.com | 100K/월 |
| **Etherscan** | etherscan.io | 5 req/sec |
| **News API** | newsapi.org | 100 req/day |
| **Reddit (praw)** | reddit.com/prefs/apps | 60 req/min |
| **Santiment** | santiment.net | GraphQL 무료 |
| **Polygon.io** | polygon.io | 5 req/min |

---

## 1. 📈 주식 (Equities)

| 소스 | 라이브러리 | 데이터 유형 | 프리 티어 한도 | API 키 |
|------|------------|-------------|---------------|--------|
| **Yahoo Finance** | `yfinance` | OHLCV, 재무제표, 배당 | 무제한 | ❌ 불필요 |
| **Alpha Vantage** | `alpha_vantage` | OHLCV, 펀더멘털, 뉴스 센티먼트 | 25 req/day | ✅ 필요 |
| **Finnhub** | `finnhub-python` | 실시간 시세, 뉴스, 펀더멘털 | 60 req/min | ✅ 필요 |
| **IEX Cloud** | `iexfinance` | 주식, 펀더멘털, 뉴스, FX | 무료 티어 | ✅ 필요 |
| **Twelve Data** | `twelvedata` | 실시간/과거 시세 | 800 req/day | ✅ 필요 |
| **Polygon.io** | `polygon` | 실시간, WebSocket | 5 req/min | ✅ 필요 |
| **FRED** | `fredapi` | 매크로 경제지표 | 무제한 | ✅ 필요 |
| **Financial Modeling Prep** | REST API | 재무제표, 비율 | 250 req/day | ✅ 필요 |
| **EODHD** | `eodhd` | EOD 데이터 | 20 req/day | ✅ 필요 |
| **Marketstack** | REST API | 70+ 글로벌 거래소 | 100 req/월 | ✅ 필요 |
| **EDGAR** | SEC 직접 | 공시자료 | 무제한 | ❌ 불필요 |
| **OpenBB** | 오픈소스 | Bloomberg 대안 터미널 | 무료 | ❌ 불필요 |
| **Koyfin** | 웹 | 차트, 뉴스, 공시 | 무료 플랜 | ❌ 불필요 |

---

## 2. 🪙 암호화폐 - 정형 데이터 (Crypto - Structured)

| 소스 | 라이브러리 | 데이터 유형 | 프리 티어 한도 | API 키 |
|------|------------|-------------|---------------|--------|
| **CCXT** | `ccxt` | OHLCV, 호가창 (100+ 거래소) | 거래소별 상이 | ❌ 불필요 |
| **Binance API** | REST/WS | 선물 OI, Funding Rate | 무제한 | ❌ 불필요 |
| **Bybit API** | REST/WS | 선물/현물 OHLCV | 무제한 | ❌ 불필요 |
| **CoinGecko** | `pycoingecko` | 마켓캡, 볼륨, 커뮤니티 | 10-30 req/min | ❌ 불필요 |
| **CryptoCompare** | `cryptocompare` | OHLCV, 소셜 | 100K req/월 | ✅ 필요 |
| **CoinPaprika** | REST API | 마켓 데이터 | 무제한 | ❌ 불필요 |
| **Messari** | REST API | 펀더멘털, 메트릭스 | 무료 티어 | ✅ 필요 |

---

## 3. ⛓️ 온체인 데이터 (On-Chain)

| 소스 | 데이터 유형 | 프리 티어 한도 | API 키 |
|------|-------------|---------------|--------|
| **Dune Analytics** | SQL 기반 온체인 쿼리 | 무제한 (공개 쿼리) | ❌ 불필요 |
| **DefiLlama** | TVL, 프로토콜 데이터 | 무제한 | ❌ 불필요 |
| **CryptoQuant** | Exchange Reserve, Whale | 기본 무료 | ✅ 필요 |
| **Glassnode** | NUPL, SOPR, Exchange Flow | 제한적 무료 | ✅ 필요 |
| **IntoTheBlock** | 홀더 분포, 대량 거래 | 기본 무료 | ✅ 필요 |
| **Santiment** | 온체인 + 소셜 + 개발 활동 | GraphQL API 무료 | ✅ 필요 |
| **Etherscan** | 지갑, 트랜잭션, 컨트랙트 | 무료 API | ✅ 필요 |
| **BscScan** | BSC 온체인 데이터 | 무료 API | ✅ 필요 |
| **Moralis** | NFT, 토큰, 스마트컨트랙트 | 관대한 무료 | ✅ 필요 |
| **Alchemy** | NFT, 토큰 메타데이터 | 무료 티어 | ✅ 필요 |
| **Bitquery** | 40+ 블록체인 | 무료 API | ✅ 필요 |
| **Covalent** | 100+ 블록체인 표준화 | 무료 티어 | ✅ 필요 |
| **QuickNode** | 온체인 데이터 | 무료 티어 | ✅ 필요 |

---

## 4. � DEX 거래소 데이터 (Decentralized Exchange)

| 소스 | 데이터 유형 | 프리 티어 한도 | API 키 | 특징 |
|------|-------------|---------------|--------|------|
| **DEX Screener** | 실시간 가격, 차트, 신규 페어 | 무제한 | ❌ 불필요 | 멀티체인 DEX 통합 |
| **GeckoTerminal** | DEX 가격, 유동성, 볼륨 | 무제한 | ❌ 불필요 | CoinGecko DEX 버전 |
| **DefiLlama DEX** | DEX 볼륨, TVL | 무제한 | ❌ 불필요 | 프로토콜별 비교 |
| **Dune (DEX)** | Swap 히스토리, 유동성 | 무제한 | ❌ 불필요 | SQL로 심층 분석 |
| **The Graph** | Uniswap/Sushi 서브그래프 | 무료 티어 | ✅ 필요 | GraphQL 쿼리 |
| **0x API** | DEX 집계, 스왑 견적 | 무제한 | ❌ 불필요 | 멀티 DEX 라우팅 |
| **1inch API** | DEX 집계, 최적 라우팅 | 무제한 | ❌ 불필요 | 가스 최적화 |
| **Uniswap Subgraph** | 풀, 스왑, 유동성 이벤트 | 무제한 | ❌ 불필요 | V2/V3 지원 |
| **SushiSwap Subgraph** | 풀, 스왑, 팜 데이터 | 무제한 | ❌ 불필요 | 멀티체인 |
| **PancakeSwap API** | BSC DEX 데이터 | 무제한 | ❌ 불필요 | BSC 최대 DEX |

### 🛠️ DEX 퀵스타트 코드 (API 키 불필요!)
```python
import requests

# DEX Screener - 실시간 가격
pair_address = "0x..."  # 페어 주소
dex = requests.get(f'https://api.dexscreener.com/latest/dex/pairs/ethereum/{pair_address}').json()

# GeckoTerminal - 트렌딩 풀
trending = requests.get('https://api.geckoterminal.com/api/v2/networks/eth/trending_pools').json()

# DefiLlama - DEX 볼륨
dex_volume = requests.get('https://api.llama.fi/overview/dexs').json()

# 1inch - 스왑 견적
quote = requests.get('https://api.1inch.dev/swap/v5.2/1/quote?src=0x...&dst=0x...&amount=1000000000000000000').json()

# Uniswap Subgraph (The Graph)
query = '''
{
  pools(first: 10, orderBy: totalValueLockedUSD, orderDirection: desc) {
    id
    token0 { symbol }
    token1 { symbol }
    totalValueLockedUSD
    volumeUSD
  }
}
'''
# https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3 에서 실행
```

### 📊 DEX 데이터 활용 전략 예시
```
1. 신규 페어 스니핑: DEX Screener 신규 페어 모니터링
2. 유동성 차익: 1inch/0x 라우팅 비교
3. 고래 스왑 추적: Dune SQL로 대형 스왑 분석
4. TVL 변화 기반: DefiLlama TVL 급증 프로토콜 탐지
5. CEX-DEX 차익: Binance vs Uniswap 가격 차이
```

---

## 5. �📰 비정형 데이터 - 센티먼트/소셜 (Sentiment/Social)

| 소스 | 데이터 유형 | 프리 티어 한도 | API 키 |
|------|-------------|---------------|--------|
| **Fear & Greed Index** | 시장 심리 지수 | 무제한 | ❌ 불필요 |
| **Google Trends** | 검색 트렌드 | 무제한 | ❌ 불필요 |
| **LunarCrush** | 소셜 메트릭스 | 제한적 무료 | ✅ 필요 |
| **CryptoPanic** | 크립토 뉴스 | 무료 API | ✅ 필요 |
| **Santiment** | 소셜 볼륨, 감성 | GraphQL 무료 | ✅ 필요 |
| **StockGeist.ai** | Discord, Telegram, Reddit | 10K 크레딧 무료 | ✅ 필요 |
| **Augmento** | 소셜 미디어 감성 | 무료 API | ✅ 필요 |
| **Alpha Vantage** | 뉴스 센티먼트 | 25 req/day | ✅ 필요 |
| **CoinDesk API** | 뉴스, 센티먼트 | 무료 티어 | ✅ 필요 |
| **News API** | 뉴스 헤드라인 | 100 req/day | ✅ 필요 |
| **Reddit** | r/Bitcoin, r/wallstreetbets | 60 req/min | ✅ 필요 |

---

## 5. 🛠️ 퀵 스타트 코드 (API 키 불필요!)

### 주식 - yfinance (API 키 없이 바로 실행)
```python
import yfinance as yf

# 즉시 사용 가능!
aapl = yf.download('AAPL', start='2020-01-01')
spy = yf.download('SPY', start='2020-01-01')
```

### 암호화폐 - CCXT + Binance (API 키 없이 바로 실행)
```python
import ccxt
import requests

# OHLCV (공개 API)
binance = ccxt.binance()
ohlcv = binance.fetch_ohlcv('BTC/USDT', '1h', limit=500)

# Funding Rate (공개 API)
url = 'https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=100'
funding = requests.get(url).json()

# Open Interest (공개 API)
oi_url = 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT'
oi = requests.get(oi_url).json()
```

### 온체인 - DefiLlama (API 키 없이 바로 실행)
```python
import requests

# TVL
tvl = requests.get('https://api.llama.fi/tvl/ethereum').json()

# 프로토콜별 TVL
protocols = requests.get('https://api.llama.fi/protocols').json()
```

### 센티먼트 - Fear & Greed + Google Trends (API 키 없이 바로 실행)
```python
import requests
from pytrends.request import TrendReq

# Fear & Greed
fng = requests.get('https://api.alternative.me/fng/?limit=30').json()

# Google Trends
pytrends = TrendReq()
pytrends.build_payload(['bitcoin'], timeframe='today 3-m')
trends = pytrends.interest_over_time()
```

---

## 6. 📁 데이터 조합 예시 (참고용, 제한 아님!)

> ⚠️ **주의**: 아래는 **예시일 뿐**! 전략에 따라 **위 목록에서 자유롭게 조합**할 것.
> Data Engineer는 **전략 목적에 맞는 최적의 데이터를 스스로 판단**하여 선택해야 함.

### 예시 1: 암호화폐 모멘텀 전략
```
CCXT(OHLCV) + Binance(Funding) + Fear&Greed
```

### 예시 2: DeFi 분석
```
DefiLlama(TVL) + Dune(온체인) + Santiment(소셜)
```

### 예시 3: 주식 펀더멘털
```
yfinance(OHLCV) + FRED(매크로) + Google Trends
```

### 예시 4: 크립토 고래 추적
```
CryptoQuant(거래소흐름) + Etherscan(지갑) + Dune(SQL)
```

---

## ⚠️ 주의사항

1. **API 키 없이 시작**: 먼저 API 키 불필요 소스로 시작, 필요 시 추가
2. **Rate Limit**: 프리 티어 한도 초과 시 IP 차단 위험
3. **Point-in-Time**: 과거 시점 데이터 보장 여부 반드시 확인
4. **Survivorship Bias**: 상장폐지/상폐 종목 누락 주의
5. **자유 선택**: 위 목록은 가이드일 뿐, **제한이 아님**
