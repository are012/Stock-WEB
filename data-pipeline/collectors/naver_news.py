import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NaverNewsCollector:
    def __init__(self):
        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")
        self.api_url = "https://openapi.naver.com/v1/search/news.json"

    def get_latest_news(self, stock_name: str, count: int = 5):
        """
        네이버 검색 API를 통해 특정 종목의 최신 뉴스 헤드라인과 요약을 가져옵니다.
        """
        if not self.client_id or not self.client_secret:
            return [{"title": "시뮬레이션 뉴스", "description": "해당 기업의 실적이 예상치를 상회할 것으로 보입니다."}]

        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        params = {
            "query": stock_name,
            "display": count,
            "sort": "sim" # 정확도순 (최신순: date)
        }

        try:
            res = requests.get(self.api_url, headers=headers, params=params)
            if res.status_code == 200:
                items = res.json().get('items', [])
                # HTML 태그 제거 및 텍스트 정제
                cleaned_news = []
                for item in items:
                    cleaned_news.append({
                        "title": item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"'),
                        "description": item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"'),
                        "link": item['link']
                    })
                return cleaned_news
            else:
                print("뉴스 검색 실패:", res.text)
                return []
        except Exception as e:
            print("API 연결 오류:", e)
            return []

# 테스트용
if __name__ == "__main__":
    news_bot = NaverNewsCollector()
    print("삼성전자 최신 뉴스:", news_bot.get_latest_news("삼성전자"))
