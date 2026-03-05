import os
import praw
from ntscraper import Nitter
from dotenv import load_dotenv

load_dotenv()

class SNSCollector:
    def __init__(self):
        # 1. Reddit 설정
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent=os.getenv("REDDIT_USER_AGENT", "TradingBot/1.0")
            )
        except:
            self.reddit = None

        # 2. X (Twitter) Scraper (Nitter 인스턴스 활용)
        self.twitter_scraper = Nitter()

    def get_reddit_sentiment(self, ticker: str, limit: int = 5):
        """특정 티커 관련 Reddit(r/wallstreetbets 등) 게시글 및 댓글 수집"""
        if not self.reddit:
            return [{"title": "Reddit Simulation", "body": f"I'm bullish on {ticker}! To the moon!"}]
        
        posts = []
        try:
            # 주식 관련 서브레딧에서 검색
            for post in self.reddit.subreddit("wallstreetbets+stocks+investing").search(ticker, limit=limit, sort="new"):
                posts.append({
                    "title": post.title,
                    "body": post.selftext[:200], # 본문 일부만 저장
                    "score": post.score
                })
        except Exception as e:
            print("Reddit 수집 실패:", e)
        return posts

    def get_twitter_trends(self, ticker: str, limit: int = 5):
        """X(Twitter)에서 특정 티커($Ticker) 검색 결과 수집"""
        try:
            # Nitter를 통해 로그인 없이 특정 해시태그/티커 검색
            query = f"${ticker}"
            tweets = self.twitter_scraper.get_tweets(query, mode='hashtag', number=limit)
            
            result = []
            for t in tweets.get('tweets', []):
                result.append({
                    "text": t['text'],
                    "date": t['date'],
                    "user": t['user']['name']
                })
            return result
        except Exception as e:
            print("X(Twitter) 수집 실패:", e)
            return []

    def get_truth_social_trends(self, ticker: str):
        """Truth Social의 실시간 트렌드 포착 (대안적 로직)"""
        # Truth Social은 공식 API가 매우 폐쇄적이므로, 
        # 현재는 시뮬레이션 데이터를 제공하거나 추후 특정 인스턴스 크롤러 연동이 필요합니다.
        return [{"text": f"Truth Social: Big things coming for {ticker} soon! #MAGA #STOCKS"}]

# 테스트용
if __name__ == "__main__":
    sns = SNSCollector()
    print("Reddit 분석:", sns.get_reddit_sentiment("NVDA"))
    # print("X(Twitter) 트렌드:", sns.get_twitter_trends("NVDA"))
