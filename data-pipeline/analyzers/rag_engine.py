from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .vector_db import VectorStorage

class RAGEngine:
    def __init__(self):
        self.vector_db = VectorStorage()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def analyze_hegemony(self, ticker: str, stock_name: str):
        """
        [RAG 기반 헤게모니 스코어링]
        1. 벡터 DB에서 해당 종목의 최신 뉴스/공시 검색
        2. LLM이 검색된 정보를 바탕으로 시장 지배력 평가
        """
        # 1. 관련 정보 검색 (Context 확보)
        context_docs = self.vector_db.query_news(ticker, f"{stock_name}의 시장 지배력, 경쟁 우위, 성장성")
        context_text = "\n".join(context_docs) if context_docs else "수집된 최신 정보가 없습니다."

        # 2. LLM 프롬프트 구성 (XAI 규약 준수)
        prompt = ChatPromptTemplate.from_template("""
        당신은 금융 분석 전문가입니다. 아래 제공된 최신 뉴스 및 공시 데이터를 바탕으로 {stock_name}({ticker})의 '헤게모니 스코어(시장 지배력)'를 산출하세요.
        
        [수집된 정보]
        {context}
        
        [분석 지침]
        1. 시장 독점력, 기술적 해자, 성장 가능성을 종합적으로 고려하세요.
        2. 0~100점 사이의 점수를 매기고, 그 이유를 '설명 가능한 AI(XAI)' 관점에서 상세히 기술하세요.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"stock_name": stock_name, "ticker": ticker, "context": context_text})
        
        return response.content

# 테스트용
if __name__ == "__main__":
    engine = RAGEngine()
    # print("삼성전자 헤게모니 분석:", engine.analyze_hegemony("005930", "삼성전자"))
