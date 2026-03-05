# 퀀트멘탈 기반 멀티 에이전트 자동매매 웹 서비스
## 프로젝트 아키텍처
- 프론트엔드: Next.js 14 + TypeScript
- 백엔드: Node.js + Express (사용자 인증, 프론트엔드 통신, 라우팅)
- AI 백엔드: Python + FastAPI
- 데이터베이스:
    - PostgreSQL
    - ChromaDB
- 배포: Docker + Kubernetes

## 공통 규약
@./docs/general-guidelines.md
@./docs/security-guidelines.md
@./docs/ai-ethics-and-trading-risk-guidelines.md

## 환경 설정
- 개발 환경: 로컬 PostgreSQL, 
- 로컬 ChromaDB, Mock 투자 API
- 테스트 환경: 인메모리 데이터베이스, 과거 주가 및 리포트 데이터를 활용한 백테스팅 시뮬레이션 환경 
- 프로덕션 환경: 클라우드 데이터베이스, 실시간 증권사 API 연동