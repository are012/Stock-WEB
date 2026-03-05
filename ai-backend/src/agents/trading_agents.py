from crewai import Agent
from ..tools.stock_tools import StockTools
from langchain_ollama import ChatOllama

class TradingAgents:
    def __init__(self):
        # 모든 에이전트가 사용할 공통 로컬 LLM 정의
        self.llm = ChatOllama(
            model="qwen3.5:9b",
            base_url="http://localhost:11434",
            temperature=0.3
        )

    def researcher_agent(self):
        return Agent(
            role='Market Researcher',
            goal='시장 뉴스 및 리포트를 분석하여 주요 이벤트와 감성 지수를 파악함',
            backstory='당신은 금융 뉴스 분석 전문가입니다. 수만 개의 기사에서 노이즈를 제거하고 실제 주가에 영향을 줄 핵심 정보만 찾아냅니다.',
            tools=[StockTools.fetch_news],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

    def technical_analyst_agent(self):
        return Agent(
            role='Technical Analyst',
            goal='차트 패턴과 기술적 지표를 분석하여 매매 시점을 포착함',
            backstory='당신은 20년 경력의 차트 분석가입니다. 주가의 흐름과 거래량 패턴에서 세력의 움직임과 추세 전환을 읽어냅니다.',
            tools=[StockTools.fetch_stock_data],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

    def financial_analyst_agent(self):
        return Agent(
            role='Financial Analyst',
            goal='재무제표와 기업 가치를 분석하여 퀀트멘탈 스코어를 산출함',
            backstory='당신은 기업의 내재 가치를 평가하는 퀀트 분석가입니다. 매출 성장성, 수익성, 시장 지배력을 숫자로 입증합니다.',
            tools=[StockTools.fetch_financials],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

    def risk_manager_agent(self):
        return Agent(
            role='Risk Manager',
            goal='모든 분석 결과의 리스크를 최종 검토하고 자산 배분 전략을 결정함',
            backstory='당신은 보수적인 리스크 관리자입니다. 다른 에이전트들의 추천이 과도한 리스크를 포함하고 있는지 검토하고 최종 승인을 내립니다.',
            llm=self.llm,
            allow_delegation=True,
            verbose=True
        )
