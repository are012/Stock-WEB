import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStorage:
    def __init__(self, collection_name="stock_news"):
        # 로컬에 데이터 저장 (data-pipeline/storage/chroma_db)
        self.client = chromadb.PersistentClient(path="./storage/chroma_db")
        
        # OpenAI 임베딩 함수 설정
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # 컬렉션 생성 또는 로드
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_news(self, ticker: str, news_list: list):
        """수집된 뉴스 리스트를 벡터 DB에 저장합니다."""
        ids = [f"{ticker}_{i}_{os.urandom(4).hex()}" for i in range(len(news_list))]
        documents = [n['description'] for n in news_list]
        metadatas = [{"ticker": ticker, "title": n['title'], "link": n['link']} for n in news_list]
        
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"✅ [{ticker}] 뉴스 {len(news_list)}건 벡터 DB 저장 완료")

    def query_news(self, ticker: str, query: str, n_results: int = 3):
        """질문과 가장 유사한 뉴스를 검색합니다 (RAG의 핵심)"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"ticker": ticker} # 특정 종목 데이터만 필터링
        )
        return results['documents'][0] if results['documents'] else []

# 테스트용
if __name__ == "__main__":
    v_db = VectorStorage()
    # 가상의 뉴스 데이터 저장 테스트
    # v_db.add_news("005930", [{"title": "반도체 호재", "description": "삼성전자가 신규 파운드리 계약을 체결했습니다.", "link": "..."}])
    print("검색 결과:", v_db.query_news("005930", "삼성전자의 파운드리 사업 전망은?"))
