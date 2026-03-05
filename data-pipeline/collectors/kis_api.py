import os
import requests
import json
import asyncio
import websockets
from dotenv import load_dotenv

# 환경변수 로드 (.env 파일에 KIS_APP_KEY, KIS_APP_SECRET 설정 필요)
load_dotenv()

class KisAPI:
    def __init__(self, is_mock=True):
        """
        is_mock=True 일 경우 모의투자 환경, False일 경우 실전투자 환경
        """
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        
        if is_mock:
            self.base_url = "https://openapivts.koreainvestment.com:29443" # 모의투자 REST
            self.ws_url = "ws://ops.koreainvestment.com:31000"           # 모의투자 WS
        else:
            self.base_url = "https://openapi.koreainvestment.com:9443"    # 실전투자 REST
            self.ws_url = "ws://ops.koreainvestment.com:21000"           # 실전투자 WS
            
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """REST API 통신을 위한 OAuth 2.0 접근 토큰 발급"""
        print("KIS API Access Token 발급 중...")
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            res = requests.post(url, headers=headers, data=json.dumps(body))
            if res.status_code == 200:
                return res.json().get("access_token")
            else:
                print("토큰 발급 실패:", res.text)
                return None
        except Exception as e:
            print("API 연결 오류 (키 설정을 확인하세요):", e)
            return "DUMMY_TOKEN" # 테스트 환경 방어 로직

    def _get_websocket_approval_key(self):
        """WebSocket 접속을 위한 승인키(Approval Key) 발급"""
        url = f"{self.base_url}/oauth2/Approval"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret
        }
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 200:
            return res.json().get("approval_key")
        return "DUMMY_APPROVAL_KEY"

    def get_current_price(self, ticker: str):
        """
        [REST API] 주식 현재가 시세 조회 (FHKST01010100)
        """
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST01010100" # 주식현재가 시세 Transaction ID
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J", # J: 주식, ETF, ETN
            "FID_INPUT_ISCD": ticker       # 종목코드 (예: 005930)
        }
        
        try:
            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                data = res.json()
                price = data.get('output', {}).get('stck_prpr') # 주식 현재가
                vol = data.get('output', {}).get('acml_vol')    # 누적 거래량
                return {"ticker": ticker, "price": price, "volume": vol}
            else:
                print(f"[{ticker}] 시세 조회 에러:", res.text)
                return None
        except Exception as e:
            return {"error": str(e)}

    async def connect_websocket(self, ticker: str):
        """
        [WebSocket API] 실시간 주식 체결가 구독 (H0STCNT0)
        """
        approval_key = self._get_websocket_approval_key()
        
        async with websockets.connect(f"{self.ws_url}/tryitout/H0STCNT0") as websocket:
            # 1. 실시간 시세 구독(등록) 요청 데이터 포맷
            subscribe_data = {
                "header": {
                    "approval_key": approval_key,
                    "custtype": "P", # P: 개인
                    "tr_type": "1",  # 1: 등록(구독 시작)
                    "content-type": "utf-8"
                },
                "body": {
                    "input": {
                        "tr_id": "H0STCNT0", # 실시간 주식 체결가
                        "tr_key": ticker     # 구독할 종목코드
                    }
                }
            }
            
            await websocket.send(json.dumps(subscribe_data))
            print(f"✅ [{ticker}] 실시간 체결가 구독을 시작합니다...")
            
            # 2. 실시간 데이터 수신 루프
            try:
                while True:
                    response = await websocket.recv()
                    # 수신된 데이터 파싱 로직 (KIS 웹소켓 데이터는 '|' 구분자로 들어옵니다)
                    if response[0] == '0' or response[0] == '1': # 일반적인 데이터 스트림
                        parts = response.split('|')
                        if len(parts) >= 4:
                            data_fields = parts[3].split('^')
                            if len(data_fields) > 11:
                                current_price = data_fields[2] # 현재가
                                print(f"🔔 [실시간] {ticker} - 현재가: {current_price}원")
                    else:
                        print("시스템 메시지:", response)
                        
            except websockets.exceptions.ConnectionClosed:
                print(f"❌ [{ticker}] 웹소켓 연결이 종료되었습니다.")

# 단독 실행 테스트 (비동기 환경)
if __name__ == "__main__":
    from ticker_mapper import TickerMapper
    
    # 1. 이름으로 종목코드 검색
    mapper = TickerMapper()
    target_name = "삼성전자"
    ticker = mapper.get_ticker(target_name)
    print(f"\n🔍 '{target_name}'의 종목코드: {ticker}")
    
    # 2. API 객체 생성 및 현재가 조회
    kis = KisAPI(is_mock=True)
    current_data = kis.get_current_price(ticker)
    print(f"\n📊 [REST API] 현재가 조회 결과: {current_data}")
    
    # 3. (옵션) 실시간 웹소켓 구독 (주석 해제 시 무한 루프 실행)
    # print("\n🚀 웹소켓 실시간 데이터 수신을 시작합니다. (종료: Ctrl+C)")
    # asyncio.get_event_loop().run_until_complete(kis.connect_websocket(ticker))
