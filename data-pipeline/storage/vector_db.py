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

    def add_document(self, ticker: str, content: str, metadata: dict):
        """
        뉴스, 리포트, 공시 등 비정형 텍스트를 풍부한 메타데이터와 함께 저장합니다.
        metadata 예시: {
            "source": "한경컨센서스",
            "author": "이베스트투자증권",
            "published_at": "2026-03-05",
            "title": "반도체 업황 분석",
            "data_type": "Report",
            "url": "..."
        }
        """
        doc_id = f"{ticker}_{metadata['data_type']}_{os.urandom(4).hex()}"
        
        # 필수 메타데이터 강제 포함
        full_metadata = {
            **metadata,
            "ticker": ticker,
            "stored_at": str(os.urandom(4).hex()) # 저장 시점 식별용
        }
        
        self.collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[full_metadata]
        )
        print(f"✅ [{ticker}] {metadata['data_type']} 데이터 저장 완료 (Source: {metadata['source']})")

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
