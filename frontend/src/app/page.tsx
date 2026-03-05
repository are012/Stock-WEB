import { TrendingUp, ShieldCheck, FileText, Activity } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AI 퀀트멘탈 트레이딩 대시보드</h1>
        <div className="status">
          <span className="signal-buy">● 실시간 가동 중</span>
        </div>
      </header>

      <div className="grid">
        {/* 포트폴리오 요약 */}
        <div className="card">
          <div className="card-title"><Activity size={20} /> 실시간 매매 시그널</div>
          <div className="content">
            <h2 className="signal-buy">STRONG BUY: 삼성전자</h2>
            <p>현재가: 73,200원 (+1.2%)</p>
            <div className="xai-logic">
              <strong>AI 판단 근거 (XAI):</strong><br />
              - Analyst Agent: 반도체 업황 턴어라운드 및 HBM 수요 증가 확인<br />
              - Chartist Agent: 20일 이동평균선 지지 후 골든크로스 발생<br />
              - Risk Manager: 변동성 대비 기대수익률(Sharpe Ratio) 2.1 달성
            </div>
          </div>
        </div>

        {/* AI 에이전트 상태 */}
        <div className="card">
          <div className="card-title"><ShieldCheck size={20} /> 멀티 에이전트 분석 현황</div>
          <ul>
            <li>Analyst: 펀더멘털 스코어 8.5/10</li>
            <li>Chartist: 기술적 지표 "상승 추세"</li>
            <li>Risk Manager: "거래 승인됨 (비중 15%)"</li>
          </ul>
        </div>

        {/* 헤게모니 리포트 */}
        <div className="card">
          <div className="card-title"><FileText size={20} /> 헤게모니 스코어링 (RAG)</div>
          <p>비정형 데이터 분석 결과 (AI 리포트 요약):</p>
          <div className="xai-logic">
            "최근 기업 컨퍼런스 콜에서 AI 가속기 시장 점유율 45% 목표를 제시함. 
            헤게모니 스코어: <strong>92점 (압도적 시장 지배력)</strong>"
          </div>
        </div>

        {/* 수익률 요약 */}
        <div className="card">
          <div className="card-title"><TrendingUp size={20} /> 누적 수익률 추이</div>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', margin: '1rem 0' }}>
            +18.4%
          </div>
          <p style={{ color: '#888' }}>지난 30일간 AI 자동매매 성과</p>
        </div>
      </div>
    </div>
  );
}
