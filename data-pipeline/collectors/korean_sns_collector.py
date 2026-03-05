import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class KoreanSNSCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_fmkorea_sentiment(self, ticker_name: str, count: int = 5):
        """
        에펨코리아 주식 갤러리 검색 결과 수집
        """
        search_url = f"https://www.fmkorea.com/index.php?act=IS&is_keyword={ticker_name}&mid=stock"
        
        try:
            res = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            posts = []
            items = soup.select('.searchResult li')
            for item in items[:count]:
                title = item.select_one('dt a')
                body = item.select_one('dd')
                if title and body:
                    posts.append({
                        "source": "FMKorea",
                        "title": title.text.strip(),
                        "body": body.text.strip()[:150],
                        "link": "https://www.fmkorea.com" + title['href']
                    })
            return posts
        except Exception as e:
            print("에펨코리아 수집 실패:", e)
            return []

    def get_arca_live_sentiment(self, ticker_name: str, count: int = 5):
        """
        아카라이브 주식 채널 검색 결과 수집
        """
        search_url = f"https://arca.live/b/stock?target=all&keyword={ticker_name}"
        
        try:
            res = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            posts = []
            items = soup.select('.vrow-inner')
            for item in items[:count]:
                title = item.select_one('.title')
                if title:
                    posts.append({
                        "source": "ArcaLive",
                        "title": title.text.strip(),
                        "body": "본문 분석 대기 중", # 목록에서 본문 추출은 별도 상세 페이지 접근 필요
                        "link": "https://arca.live" + title['href']
                    })
            return posts
        except Exception as e:
            print("아카라이브 수집 실패:", e)
            return []

    def get_toss_sentiment(self, ticker_name: str):
        """
        토스 커뮤니티의 실시간 반응 (시뮬레이션 로직)
        실제 토스는 API 구조가 폐쇄적이므로 패턴화된 시뮬레이션 데이터를 제공하거나 전용 크롤러 사용
        """
        return [{
            "source": "Toss",
            "title": f"토스인들 {ticker_name}에 관심 집중!",
            "body": "실시간 매수세가 강해지고 있습니다. 토스 게시판 분위기 매우 좋음.",
            "link": "https://toss.im"
        }]

# 테스트용
if __name__ == "__main__":
    collector = KoreanSNSCollector()
    print("에펨코리아 분석:", collector.get_fmkorea_sentiment("삼성전자"))
    # print("아카라이브 분석:", collector.get_arca_live_sentiment("삼성전자"))
