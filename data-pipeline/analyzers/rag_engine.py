from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..storage.vector_db import VectorStorage
from ..collectors.naver_news import NaverNewsCollector
from ..collectors.report_collector import ReportCollector

class HybridRAGEngine:
    def __init__(self):
        self.vector_db = VectorStorage()
        self.news_collector = NaverNewsCollector()
        self.report_collector = ReportCollector()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def analyze_stock_hybrid(self, ticker: str, stock_name: str):
        """
        [하이브리드 RAG 분석]
        1. 과거 맥락: 벡터 DB에서 최근 리포트/공시 검색 (중장기 펀더멘털)
        2. 실시간 감각: 네이버 뉴스에서 즉시 속보 검색 (단기 모멘텀)
        3. 통합 분석: 두 정보를 결합하여 최종 '헤게모니 스코어' 산출
        """
        print(f"🔍 [{stock_name}] 하이브리드 분석 엔진 가동 중...")

        # 1. 과거 지식 검색 (Vector DB - 리포트, 공시 등)
        past_context_docs = self.vector_db.query_news(ticker, f"{stock_name}의 시장 지배력, 경쟁 우위, 기업 가치 분석")
        past_context = "\n".join(past_context_docs) if past_context_docs else "과거 축적된 분석 데이터가 없습니다."

        # 2. 실시간 속보 검색 (Naver News - 즉시 크롤링)
        live_news = self.news_collector.get_latest_news(stock_name, count=3)
        live_context = "\n".join([f"제목: {n['title']} / 내용: {n['description']}" for n in live_news]) if live_news else "실시간 속보가 없습니다."

        # 3. 통합 프롬프트 구성
        prompt = ChatPromptTemplate.from_template("""
        당신은 최고의 금융 전략가입니다. 아래의 **중장기 분석 데이터(과거)**와 **실시간 속보(현재)**를 결합하여 {stock_name}({ticker})에 대한 최종 투자의견을 내세요.
        
        [중장기 분석 및 공시 (과거 맥락)]
        {past_context}
        
        [실시간 속보 및 여론 (현재 이슈)]
        {live_context}
        
        [분석 지침]
        1. 과거의 중장기적 강점(해자)이 현재의 속보로 인해 훼손되었는지, 혹은 강화되었는지 판단하세요.
        2. '헤게모니 스코어(0~100)'를 산출하고, 그 이유를 '설명 가능한 AI(XAI)' 관점에서 논리적으로 기술하세요.
        3. 최종 결정(매수/홀딩/매도)을 제안하세요.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "stock_name": stock_name, 
            "ticker": ticker, 
            "past_context": past_context,
            "live_context": live_context
        })
        
        return response.content

# 테스트용
if __name__ == "__main__":
    engine = HybridRAGEngine()
    # result = engine.analyze_stock_hybrid("005930", "삼성전자")
    # print(result)
