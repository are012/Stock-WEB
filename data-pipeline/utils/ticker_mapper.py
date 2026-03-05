import FinanceDataReader as fdr

class TickerMapper:
    def __init__(self):
        print("한국거래소(KRX) 종목 마스터 데이터를 불러오는 중...")
        # KRX (KOSPI, KOSDAQ, KONEX) 전체 상장 종목 로드
        self.df_krx = fdr.StockListing('KRX')
    
    def get_ticker(self, name: str) -> str:
        """
        사용자 입력을 바탕으로 종목 코드(티커)를 반환합니다.
        예: '삼성전자' -> '005930'
        """
        # 1. 정확히 일치하는 이름 검색
        result = self.df_krx[self.df_krx['Name'] == name]
        if not result.empty:
            return result.iloc[0]['Code']
        
        # 2. 정확히 일치하지 않을 경우, 포함하는 이름 검색 (부분 일치)
        result_partial = self.df_krx[self.df_krx['Name'].str.contains(name, na=False)]
        if not result_partial.empty:
            best_match = result_partial.iloc[0]['Name']
            code = result_partial.iloc[0]['Code']
            print(f"[{name}] 정확한 일치 항목이 없습니다. 가장 유사한 종목으로 대체합니다: {best_match} ({code})")
            return code
            
        raise ValueError(f"'{name}'에 해당하는 종목을 찾을 수 없습니다.")

# 단독 실행 테스트용
if __name__ == "__main__":
    mapper = TickerMapper()
    print("삼성전자 티커:", mapper.get_ticker("삼성전자"))
    print("카카오 티커:", mapper.get_ticker("카카오"))
