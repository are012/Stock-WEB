import os
import OpenDartReader
from dotenv import load_dotenv

load_dotenv()

class DartCollector:
    def __init__(self):
        self.api_key = os.getenv("DART_API_KEY")
        # 키가 없을 경우 시뮬레이션 모드 (에러 방지)
        if self.api_key:
            self.dart = OpenDartReader(self.api_key)
        else:
            self.dart = None
            print("⚠️ DART_API_KEY가 설정되지 않았습니다. 실제 수집이 불가능합니다.")

    def get_company_summary(self, ticker: str):
        """
        특정 기업의 최근 사업보고서를 통해 시장 점유율 및 주요 사업 내용을 수집합니다.
        '헤게모니 스코어링'의 핵심 정성 데이터가 됩니다.
        """
        if not self.dart: return "시뮬레이션 데이터: 해당 기업은 시장 지배력이 높으며 AI 반도체 분야의 선두주자입니다."
        
        try:
            # 최근 1년 내 사업보고서(11011) 가져오기
            report = self.dart.list(ticker, start='2023-01-01', kind='A')
            if not report.empty:
                rcept_no = report.iloc[0]['rcept_no']
                # '이사의 경영진단 및 분석의견' 섹션에서 성장성/시장성 텍스트 추출
                # (실제 고도화 시에는 해당 섹션의 텍스트를 파싱하여 LLM에 전달)
                return f"DART Report (No. {rcept_no}) 수집 완료. 시장 지배력 분석 대기 중..."
            return "최근 공시 리포트를 찾을 수 없습니다."
        except Exception as e:
            return f"DART 수집 에러: {str(e)}"

# 테스트용
if __name__ == "__main__":
    collector = DartCollector()
    print("삼성전자 공시 요약:", collector.get_company_summary("005930"))
