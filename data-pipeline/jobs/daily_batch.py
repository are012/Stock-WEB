import sys
import os
import time
from datetime import datetime

# 프로젝트 루트를 경로에 추가 (모듈 임포트용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collectors.kis_api import KisAPI
from collectors.dart_api import DartCollector
from collectors.naver_news import NaverNewsCollector
from collectors.sns_collector import SNSCollector
from collectors.report_collector import ReportCollector
from collectors.macro_collector import MacroCollector
from utils.ticker_mapper import TickerMapper
from storage.vector_db import VectorStorage

class DailyBatchJob:
    def __init__(self):
        print(f"🚀 [{datetime.now()}] 퀀트멘탈 통합 데이터 파이프라인 가동 시작...")
        self.v_db = VectorStorage()
        self.mapper = TickerMapper()
        
        # 수집기 초기화
        self.kis = KisAPI(is_mock=True)
        self.dart = DartCollector()
        self.naver = NaverNewsCollector()
        self.sns = SNSCollector()
        self.report = ReportCollector()
        self.macro = MacroCollector()

    def process_stock(self, stock_name: str):
        """특정 종목에 대한 모든 데이터를 수집하고 벡터 DB에 저장합니다."""
        print(f"\n--- [{stock_name}] 분석 데이터 수집 시작 ---")
        try:
            ticker = self.mapper.get_ticker(stock_name)
            
            # 1. 네이버 뉴스 수집 및 저장
            news_list = self.naver.get_latest_news(stock_name, count=5)
            for news in news_list:
                self.v_db.add_document(ticker, news['description'], {
                    "source": "Naver News",
                    "title": news['title'],
                    "published_at": datetime.now().strftime("%Y-%m-%d"),
                    "data_type": "News",
                    "url": news['link']
                })

            # 2. 증권사 리포트 수집 및 저장
            reports = self.report.get_latest_reports(stock_name, count=2)
            for r in reports:
                content = self.report.extract_text_from_pdf(r['pdf_url'])
                if content:
                    self.v_db.add_document(ticker, content[:2000], { # 핵심 내용 위주
                        "source": r['broker'],
                        "title": r['title'],
                        "published_at": r['date'],
                        "data_type": "Report",
                        "url": r['pdf_url'],
                        "opinion": r['opinion'],
                        "target_price": r['target_price']
                    })

            # 3. DART 공시 요약 저장
            dart_summary = self.dart.get_company_summary(ticker)
            self.v_db.add_document(ticker, dart_summary, {
                "source": "DART",
                "title": f"{stock_name} 최근 공시 요약",
                "published_at": datetime.now().strftime("%Y-%m-%d"),
                "data_type": "Disclosure",
                "url": "https://dart.fss.or.kr"
            })

            # 4. SNS 여론(Reddit 등) 저장
            reddit_posts = self.sns.get_reddit_sentiment(ticker, limit=3)
            for p in reddit_posts:
                self.v_db.add_document(ticker, p['body'], {
                    "source": "Reddit",
                    "title": p['title'],
                    "published_at": datetime.now().strftime("%Y-%m-%d"),
                    "data_type": "SNS",
                    "score": str(p['score'])
                })

            print(f"✅ [{stock_name}] 데이터 파이프라인 처리 완료")

        except Exception as e:
            print(f"❌ [{stock_name}] 처리 중 오류 발생: {e}")

    def run_macro_update(self):
        """시장 매크로 지표 업데이트"""
        print("\n--- 거시 경제(Macro) 지표 업데이트 중 ---")
        status = self.macro.get_macro_status()
        # 매크로 지표는 별도의 메타데이터로 관리하거나 텍스트화하여 저장 가능
        macro_text = str(status)
        self.v_db.add_document("GLOBAL", macro_text, {
            "source": "Yahoo Finance",
            "title": "Global Macro Status",
            "published_at": datetime.now().strftime("%Y-%m-%d"),
            "data_type": "Macro",
            "url": "N/A"
        })

    def execute_all(self, target_stocks: list):
        """전체 종목 및 매크로 배치 실행"""
        self.run_macro_update()
        for stock in target_stocks:
            self.process_stock(stock)
            time.sleep(1) # API 호출 간격 조절 (Rate Limit 방지)
        print(f"\n✨ [{datetime.now()}] 모든 배치 작업이 성공적으로 완료되었습니다.")

if __name__ == "__main__":
    # 분석 대상 종목 리스트 (관심 종목 위주로 시작)
    targets = ["삼성전자", "SK하이닉스", "카카오", "현대차", "NAVER"]
    
    batch = DailyBatchJob()
    batch.execute_all(targets)
