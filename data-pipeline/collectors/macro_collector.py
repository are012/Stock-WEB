import yfinance as yf
import pandas as pd

class MacroCollector:
    def __init__(self):
        # 주요 거시지표 티커 정의
        self.macro_tickers = {
            "USD/KRW": "KRW=X",        # 원/달러 환율
            "S&P 500": "^GSPC",        # 미국 S&P 500 지수
            "KOSPI": "^KS11",          # 코스피 지수
            "WTI Oil": "CL=F",         # 서부 텍스트유 가격
            "US 10Y Bond": "^TNX",     # 미국 10년물 국채 금리
            "KOSDAQ": "^KQ11"          # 코스닥 지수
        }

    def get_macro_status(self):
        """
        주요 거시지표의 현재가와 전일 대비 등락률을 수집합니다.
        에이전트가 "시장 분위기가 좋은가?"를 판단하는 척도가 됩니다.
        """
        results = {}
        for name, ticker in self.macro_tickers.items():
            try:
                data = yf.Ticker(ticker).history(period="2d")
                if len(data) >= 2:
                    current = data['Close'].iloc[-1]
                    prev = data['Close'].iloc[-2]
                    change = ((current - prev) / prev) * 100
                    results[name] = {"price": round(current, 2), "change": round(change, 2)}
            except Exception as e:
                print(f"[{name}] 수집 실패:", e)
        return results

# 테스트용
if __name__ == "__main__":
    macro = MacroCollector()
    print("실시간 거시 경제 현황:", macro.get_macro_status())
