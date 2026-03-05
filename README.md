# 📈 QuantMental: AI 멀티 에이전트 자동매매 시스템

본 프로젝트는 정량적 지표(Quant)와 정성적 분석(Fundamental)을 결합한 **'퀀트멘탈'** 접근법을 기반으로 하는 차세대 자동매매 웹 서비스입니다. 

외부 유료 API 의존성을 최소화하고 **Ollama 기반의 로컬 AI 인프라**를 활용하여 강력한 보안과 저비용 고성능 분석 환경을 구축했습니다.

---

## 🏗️ 시스템 아키텍처

- **Frontend**: Next.js 14 (App Router) + TypeScript + Lucide React (대시보드 UI)
- **Backend**: Node.js (Express) - 사용자 요청 처리 및 API 브릿지
- **AI Engine**: Python (CrewAI) - 멀티 에이전트 협업 및 하이브리드 RAG 분석
- **Data Pipeline**: Python - 전방위 데이터 수집 (KIS, DART, 네이버, 한국형 SNS 등)
- **Local AI**: Ollama (LLM: Qwen 3.5 9B, Embedding: Jina Embeddings v5)
- **Database**: 
  - **Vector DB**: ChromaDB (뉴스, 리포트, 공시 비정형 데이터 저장)
  - **RDB**: PostgreSQL (시세, 수급 데이터 저장)

---

## 🌟 핵심 기능

### 1. 하이브리드 RAG (Retrieval-Augmented Generation)
- **과거 지식**: 벡터 DB에 축적된 전문가 리포트 및 공시 데이터 활용.
- **실시간 속보**: 분석 요청 시점의 실시간 네이버 뉴스를 즉시 크롤링하여 통합 분석.

### 2. 한국 시장 특화 데이터 수집
- **여론 분석**: 에펨코리아(주식갤), 아카라이브(주식채널), 토스 커뮤니티의 실시간 여론 수집.
- **전문가 통찰**: 한경 컨센서스 증권사 리포트 PDF 마이닝.

---

## 🚀 설치 및 실행 가이드

### 1. 로컬 AI 모델 준비 (Ollama)

Ollama에서 최신 Qwen 모델과 Jina 임베딩 모델을 준비합니다.

```bash
# LLM: Qwen 3.5 (9B)
ollama pull qwen3.5:9b

# Embedding: Jina Embeddings v2/v5 (Small)
ollama pull jina/jina-embeddings-v2-base-en
```
*참고: `jina-embeddings-v5-text-small`을 직접 GGUF로 등록하여 사용할 수도 있습니다.*

### 2. 환경 변수 설정
최상위 디렉토리에 `.env` 파일을 생성하고 KIS, DART, Naver API 키를 입력하세요.

### 3. 데이터 파이프라인 가동 (인덱싱)
```bash
cd data-pipeline
pip install -r requirements.txt
python jobs/daily_batch.py
```

### 4. 개발 서버 실행
```bash
# 최상위 디렉토리에서
npm run all:dev
```

---

## 📁 디렉토리 구조
- `frontend/`: Next.js 대시보드
- `backend/`: Express 서버
- `ai-backend/`: CrewAI 에이전트 로직
- `data-pipeline/`: 통합 수집기 및 RAG 엔진
