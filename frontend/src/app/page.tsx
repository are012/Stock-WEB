"use client";

import { useState } from "react";
import { TrendingUp, ShieldCheck, Activity, Play, Zap } from "lucide-react";

export default function Dashboard() {
  const [ticker, setTicker] = useState("삼성전자");
  const [decision, setDecision] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:4000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker })
      });
      const result = await response.json();
      setDecision(result);
    } catch (error) {
      console.error("분석 실패:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>퀀트멘탈 AI 트레이딩 시스템</h1>
        <div className="status">
          <input 
            type="text" 
            value={ticker} 
            onChange={(e) => setTicker(e.target.value)}
            style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #333', background: '#222', color: '#fff' }}
          />
          <button 
            onClick={handleAnalyze}
            disabled={loading}
            style={{ marginLeft: '1rem', padding: '0.5rem 1rem', background: '#0070f3', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            {loading ? <Activity size={16} className="animate-spin" /> : <Play size={16} />}
            {loading ? '분석 중...' : 'AI 분석'}
          </button>
        </div>
      </header>

      <div className="grid">
        {/* 분석 결과 */}
        <div className="card">
          <div className="card-title"><Zap size={20} color="#00ff88" /> AI 실시간 분석 결과</div>
          <div className="content">
            {decision ? (
              <>
                <h2 className={decision.decision === "BUY" ? "signal-buy" : "signal-sell"}>
                  {decision.decision}: {decision.ticker}
                </h2>
                <div style={{ margin: '1rem 0' }}>
                  <strong>AI 스코어: {decision.score}점</strong>
                  <p style={{ fontSize: '0.9rem', color: '#ccc' }}>{decision.reason}</p>
                </div>
              </>
            ) : (
              <p>종목을 입력하고 AI 분석을 시작하세요.</p>
            )}
          </div>
        </div>

        {/* 시스템 아키텍처 정보 */}
        <div className="card">
          <div className="card-title"><ShieldCheck size={20} /> 로컬 가동 인프라</div>
          <p style={{ fontSize: '0.85rem', color: '#888' }}>
            이 시스템은 고성능 Express 백엔드와 Next.js 14 프론트엔드로 구성된 하이브리드 자동매매 시스템입니다.
          </p>
          <div className="xai-logic">
            - 백엔드: Node.js (Express)<br />
            - 데이터베이스: PostgreSQL (Local)<br />
            - 통신 방식: RESTful API (CORS 활성화)
          </div>
        </div>
      </div>
    </div>
  );
}
