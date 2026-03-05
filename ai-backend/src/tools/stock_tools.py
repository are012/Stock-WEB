import yfinance as ticker_info
from langchain.tools import tool
import pandas as pd

class StockTools:
    @tool("fetch_stock_data")
    def fetch_stock_data(ticker: str):
        """특정 종목의 최근 주가와 기술적 지표 계산을 위한 데이터를 가져옵니다."""
        stock = ticker_info.Ticker(ticker)
        hist = stock.history(period="1mo")
        return hist.to_string()

    @tool("fetch_financials")
    def fetch_financials(ticker: str):
        """특정 종목의 PER, PBR, ROE 및 주요 재무제표 데이터를 가져옵니다."""
        stock = ticker_info.Ticker(ticker)
        info = stock.info
        financials = {
            "PER": info.get("trailingPE"),
            "PBR": info.get("priceToBook"),
            "ROE": info.get("returnOnEquity"),
            "Market Cap": info.get("marketCap"),
            "Debt to Equity": info.get("debtToEquity")
        }
        return str(financials)

    @tool("fetch_news")
    def fetch_news(ticker: str):
        """특정 종목의 최신 뉴스 헤드라인과 내용을 가져옵니다."""
        stock = ticker_info.Ticker(ticker)
        news = stock.news[:5] # 최신 뉴스 5건
        formatted_news = []
        for n in news:
            formatted_news.append(f"Title: {n['title']}\nPublisher: {n['publisher']}\nLink: {n['link']}\n")
        return "\n".join(formatted_news)
