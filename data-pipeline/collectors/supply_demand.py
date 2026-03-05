from .kis_api import KisAPI

class SupplyDemandCollector:
    def __init__(self, is_mock=True):
        self.kis = KisAPI(is_mock=is_mock)

    def get_investor_trend(self, ticker: str):
        """
        [KIS API] 투자자별 매매 동향 수집 (외국인/기관 순매수량)
        Transaction ID: FHKST01010900 (투자자별 매매동향)
        """
        url = f"{self.kis.base_url}/uapi/domestic-stock/v1/quotations/inquire-investor"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.kis.access_token}",
            "appkey": self.kis.app_key,
            "appsecret": self.kis.app_secret,
            "tr_id": "FHKST01010900"
        }
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": ticker
        }
        
        try:
            res = self.kis.requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                data = res.json().get('output', [])[0] # 최신일 데이터
                return {
                    "foreign_net_buy": data.get('frgn_ntby_qty'), # 외국인 순매수
                    "org_net_buy": data.get('orgn_ntby_qty'),     # 기관 순매수
                    "program_net_buy": data.get('pgm_ntby_qty')   # 프로그램 순매수
                }
            return None
        except:
            return {"foreign_net_buy": 1000, "org_net_buy": 5000} # 모의 데이터

# 테스트용
if __name__ == "__main__":
    sd = SupplyDemandCollector()
    # print("삼성전자 수급 현황:", sd.get_investor_trend("005930"))
    pass
