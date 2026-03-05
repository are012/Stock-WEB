# AI 백엔드 개발 규약 (Python)

## 기술 스택
- 프레임워크: FastAPI
- 에이전트 프레임워크: LangChain / Custom Orchestrator
- DB: SQLAlchemy, ChromaDB (Vector DB)

## 멀티 에이전트 설계
- Analyst: 펀더멘털 분석
- Chartist: 차트 기술적 분석
- Risk Manager: 리스크 관리 및 최종 매매 승인

## RAG 및 스코어링
- 헤게모니 스코어링 모델: 비정형 데이터 기반 성장성 평가
- ChromaDB 연동 실시간 데이터 파이프라인 구축
