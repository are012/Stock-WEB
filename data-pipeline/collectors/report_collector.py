import requests
from bs4 import BeautifulSoup
import fitz # PyMuPDF
import io

class ReportCollector:
    def __init__(self):
        # 한경 컨센서스 종목 리포트 검색 URL
        self.hk_url = "http://consensus.hankyung.com/apps.analysis/analysis.list?skinType=stock"

    def get_latest_reports(self, stock_name: str, count: int = 3):
        """
        한경 컨센서스에서 특정 종목의 최신 리포트 목록을 가져옵니다.
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        params = {'search_text': stock_name}
        
        try:
            res = requests.get(self.hk_url, headers=headers, params=params)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            reports = []
            table_rows = soup.select('.table_style01 tbody tr')
            
            for row in table_rows[:count]:
                cols = row.find_all('td')
                if len(cols) > 5:
                    report_info = {
                        "date": cols[0].text.strip(),
                        "title": cols[1].text.strip(),
                        "broker": cols[2].text.strip(), # 증권사
                        "opinion": cols[3].text.strip(), # 매수/중립
                        "target_price": cols[4].text.strip(), # 목표주가
                        "pdf_url": "http://consensus.hankyung.com" + cols[8].find('a')['href'] if cols[8].find('a') else None
                    }
                    reports.append(report_info)
            return reports
        except Exception as e:
            print(f"[{stock_name}] 리포트 수집 실패:", e)
            return []

    def extract_text_from_pdf(self, pdf_url: str):
        """PDF URL에서 텍스트 본문을 추출합니다."""
        if not pdf_url: return ""
        
        try:
            response = requests.get(pdf_url)
            pdf_file = io.BytesIO(response.content)
            doc = fitz.open(stream=pdf_file, filetype="pdf")
            
            text = ""
            # 첫 2페이지만 추출 (핵심 요약 위주)
            for page in doc[:2]:
                text += page.get_text()
            return text
        except Exception as e:
            print("PDF 텍스트 추출 실패:", e)
            return ""

# 테스트용
if __name__ == "__main__":
    collector = ReportCollector()
    reports = collector.get_latest_reports("삼성전자")
    print("최신 리포트 목록:", reports)
    if reports and reports[0]['pdf_url']:
        # print("리포트 요약:", collector.extract_text_from_pdf(reports[0]['pdf_url'])[:500])
        pass
