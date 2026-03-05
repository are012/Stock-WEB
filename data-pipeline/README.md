# 퀀트멘탈(QuantMental) 데이터 파이프라인

이 디렉토리는 정량적 지표(Quant)와 정성적 분석(Fundamental/Mental) 데이터를 수집, 처리, 분석하는 파이프라인을 관리합니다.

## 📂 폴더 구조 및 역할

### 1. `collectors/` (데이터 수집)
- `stock_api.py`: 증권사 API 연동 (KOSPI/KOSDAQ 시세, 거래량)
- `financial_reports.py`: 재무제표 수집 (PBR, PER, ROE 등)
- `news_scraper.py`: 경제 뉴스 및 기업 리포트 비정형 데이터 수집 (Hegemony 분석용)

### 2. `transformers/` (데이터 변환)
- `cleaner.py`: 결측치 처리 및 데이터 정규화
- `quant_indicator.py`: 이동평균선, RSI, 볼린저 밴드 등 기술적 지표 계산

### 3. `analyzers/` (핵심 분석 엔진)
- `hegemony_scorer.py`: NLP/RAG 기반 기업 시장 지배력(Hegemony) 점수 산출
- `backtester.py`: 과거 데이터 기반 전략 성과 검증

### 4. `storage/` (데이터 저장 및 스키마)
- `vector_db.py`: ChromaDB 등 벡터 DB 연동 (비정형 데이터 검색용)
- `schema.sql`: PostgreSQL 테이블 정의서 (매매 기록, 지표 저장)

### 5. `jobs/` (스케줄링)
- `daily_batch.py`: 매일 장 마감 후 일일 지표 업데이트 및 분석 실행
- `realtime_stream.py`: 장 중 실시간 시그널 포착 및 백엔드 알림 전송

## 🛠 실행 가이드
- 각 모듈은 독립적으로 실행 가능하며, `jobs/`를 통해 통합 스케줄링됩니다.
- 분석된 결과는 데이터베이스(PostgreSQL/ChromaDB)에 저장되어 백엔드 API에서 즉시 조회 가능합니다.
