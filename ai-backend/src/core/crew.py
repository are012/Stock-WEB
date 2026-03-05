from crewai import Crew, Process, Task
from .trading_agents import TradingAgents

class TradingCrew:
    def __init__(self, ticker):
        self.ticker = ticker
        self.agents = TradingAgents()

    def run(self):
        # 1. 에이전트 생성
        researcher = self.agents.researcher_agent()
        technical = self.agents.technical_analyst_agent()
        financial = self.agents.financial_analyst_agent()
        risk_manager = self.agents.risk_manager_agent()

        # 2. 태스크 정의 (Hegemony Scoring 규약 반영)
        research_task = Task(
            description=f"{self.ticker}에 대한 최신 뉴스, 공시, 시장 리포트를 분석하여 시장 지배력(해자)과 미래 성장성을 평가하시오.",
            expected_output="뉴스 감성 지수 및 텍스트 기반 헤게모니 분석 결과 요약",
            agent=researcher
        )

        financial_task = Task(
            description=f"{self.ticker}의 재무제표를 바탕으로 PBR, PER, ROE 등 퀀트 지표를 산출하고 기업 가치를 평가하시오.",
            expected_output="정량적 퀀트 스코어 및 재무 분석 보고서",
            agent=financial
        )

        technical_task = Task(
            description=f"{self.ticker}의 차트 데이터(이동평균선, RSI, 볼린저 밴드 등)를 분석하여 매매 시그널을 생성하시오.",
            expected_output="기술적 매수/매도/홀딩 시그널 및 근거 데이터",
            agent=technical
        )

        risk_task = Task(
            description=f"앞선 모든 분석 결과를 바탕으로 최종 투자 결정을 내리시오. Sharpe Ratio 및 자산 배분 원칙을 준수해야 함.",
            expected_output="최종 결정(BUY/SELL/HOLD), 비중, XAI 근거 설명",
            agent=risk_manager
        )

        # 3. 크루 구성 및 실행 (순차적 프로세스)
        crew = Crew(
            agents=[researcher, financial, technical, risk_manager],
            tasks=[research_task, financial_task, technical_task, risk_task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()
